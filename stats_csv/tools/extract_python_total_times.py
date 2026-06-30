from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


CP_TOTAL_TIME_RE = re.compile(r"Total time:\s*([0-9.]+)\s*s")
CARD_TOTAL_TIME_RE = re.compile(r"Total time:\s*([0-9.]+)\s*seconds")
LEGACY_TOTAL_TIME_USED_RE = re.compile(r"Total time used:\s*([0-9.]+)\s*sec")
TIME_TAKEN_RE = re.compile(r"Time taken:\s*([0-9.]+)\s*(?:s|seconds)")
OBJECTIVE_VALUE_RE = re.compile(r"Objective value:\s*([0-9.]+)")
LABEL_COUNT_RE_LIST = [
    re.compile(r"Number of lables used:\s*(\d+)"),
    re.compile(r"Number of labels used:\s*(\d+)"),
    re.compile(r"Num labels used:\s*(\d+)"),
]
TRYING_SOLUTION_RE = re.compile(r"Trying with at most\s+(\d+)\s+labels\.\.\.\s*Solution:", re.IGNORECASE)
CPLEX_CP_STAR_OBJECTIVE_RE = re.compile(r"^\s*\*\s+(\d+)\s", re.MULTILINE)
CPLEX_CP_BEST_OBJECTIVE_RE = re.compile(r"Best objective\s*:\s*([0-9.]+)")
EVALMAXSAT_TOTAL_TIME_RE = re.compile(r"c Total time\s*:\s*([0-9.]+)\s*s")
EVALMAXSAT_STATUS_RE = re.compile(r"^s\s+(.+)$", re.MULTILINE)
EVALMAXSAT_OBJECTIVE_RE = re.compile(r"^o\s+(\d+)$", re.MULTILINE)
EVALMAXSAT_INFO_STATUS_RE = re.compile(r"\[INFO\]\s+status=([^,\n]+)")
EVALMAXSAT_INFO_OBJECTIVE_RE = re.compile(r"\[INFO\].*?\bobjective=(\d+)")
EVALMAXSAT_INFO_LABELS_RE = re.compile(r"\[INFO\].*?\blabels_used=(\d+)")
RUNLIM_REAL_RE = re.compile(r"\[runlim\]\s+real:\s*([0-9.]+)\s+seconds")


def last_float(pattern: re.Pattern[str], text: str) -> float | None:
    matches = pattern.findall(text)
    if not matches:
        return None
    return float(matches[-1])


def last_int(patterns: list[re.Pattern[str]], text: str) -> int | None:
    last_value: int | None = None
    last_end = -1
    for pattern in patterns:
        for match in pattern.finditer(text):
            if match.end() >= last_end:
                last_value = int(match.group(1))
                last_end = match.end()
    return last_value


def last_incumbent_label_value(text: str) -> int | None:
    explicit_value = last_int(LABEL_COUNT_RE_LIST, text)
    trying_values = [int(value) for value in TRYING_SOLUTION_RE.findall(text)]

    candidates = []
    if explicit_value is not None:
        candidates.append(explicit_value)
    candidates.extend(trying_values)
    return min(candidates) if candidates else None


def parse_cplex_cp_objective(text: str) -> int | None:
    best_objective = last_float(CPLEX_CP_BEST_OBJECTIVE_RE, text)
    if best_objective is not None:
        return int(best_objective)

    star_matches = CPLEX_CP_STAR_OBJECTIVE_RE.findall(text)
    if star_matches:
        return int(star_matches[-1])

    return None


def has_runlim_timeout(text: str) -> bool:
    return bool(re.search(r"\[runlim\]\s+status:\s+out of time", text))


def has_runlim_oom(text: str) -> bool:
    return bool(re.search(r"\[runlim\]\s+status:\s+out of memory", text))


def dataset_sort_key(name: str) -> tuple[int, int, str]:
    lowered = name.lower()
    if lowered.startswith("scen"):
        group = 0
    elif lowered.startswith("graph"):
        group = 1
    elif lowered.startswith("tud"):
        group = 2
    else:
        group = 3
    match = re.search(r"(\d+)", lowered)
    number = int(match.group(1)) if match else 10**9
    return group, number, lowered


def parse_cpsat_log(log_path: Path, preprocessing: bool, method: str, variant: str) -> dict[str, object]:
    text = log_path.read_text(encoding="utf-8", errors="ignore")

    timeout = has_runlim_timeout(text)
    oom = has_runlim_oom(text)
    if timeout:
        status = "timeout"
    elif oom:
        status = "out_of_memory"
    elif "Status: OPTIMAL" in text:
        status = "optimal"
    elif "Status: FEASIBLE" in text:
        status = "feasible"
    elif "Status: INFEASIBLE" in text or "Cannot find solution!" in text or "No solution found." in text:
        status = "infeasible"
    else:
        status = "unknown"

    total_time = last_float(CP_TOTAL_TIME_RE, text)
    time_taken = last_float(TIME_TAKEN_RE, text)
    label_value = last_incumbent_label_value(text)
    objective_value = last_float(OBJECTIVE_VALUE_RE, text)

    report_value = None
    if not oom and status in {"optimal", "feasible", "timeout"}:
        if label_value is not None:
            report_value = label_value
        elif objective_value is not None:
            report_value = int(objective_value)

    if timeout:
        report_time = 600.0
        report_time_rule = "runlim_timeout_cap"
    elif total_time is not None:
        report_time = total_time
        report_time_rule = "python_total_time"
    elif status == "infeasible" and time_taken is not None:
        report_time = time_taken
        report_time_rule = "python_early_exit_time_taken"
    else:
        report_time = None
        report_time_rule = "missing"

    return {
        "source_family": "current",
        "method": method,
        "variant": variant,
        "preprocessing": "on" if preprocessing else "off",
        "dataset": log_path.stem,
        "status": status,
        "report_value": report_value,
        "report_time_s": report_time,
        "report_time_rule": report_time_rule,
        "python_e2e_time_s": total_time if total_time is not None else report_time,
        "time_taken_s": time_taken,
        "total_time_s": total_time,
        "time_taken_role": "incumbent_callback" if time_taken is not None else "",
        "timeout_limit_s": 600.0 if timeout else None,
        "log_path": str(log_path),
    }


def parse_cardinality_log(
    log_path: Path,
    preprocessing: bool,
    variant: str,
    method: str = "cardinality",
) -> dict[str, object]:
    text = log_path.read_text(encoding="utf-8", errors="ignore")

    has_solution = "Solution:" in text
    has_cannot_find = "Cannot find solution." in text or "Cannot find solution!" in text
    has_optimal_line = "Optimal number of labels used" in text
    timeout = has_runlim_timeout(text)
    oom = has_runlim_oom(text)
    infeasible = bool(
        re.search(r"Solve first problem:\s*Cannot find solution\.", text)
        or (has_cannot_find and not has_solution)
        or "Warning: variable" in text
        or "No solution found in the preprocessing step!" in text
    )

    if timeout:
        status = "timeout"
    elif oom:
        status = "out_of_memory"
    elif has_optimal_line or (has_solution and has_cannot_find):
        status = "optimal"
    elif infeasible:
        status = "infeasible"
    else:
        status = "unknown"

    total_time = last_float(CARD_TOTAL_TIME_RE, text)
    time_taken = last_float(TIME_TAKEN_RE, text)
    label_value = last_incumbent_label_value(text)
    optimal_value_match = re.search(r"Optimal number of labels used:\s*(\d+)", text)

    report_value = None
    if not oom:
        if status == "optimal":
            if optimal_value_match is not None:
                report_value = int(optimal_value_match.group(1))
            else:
                report_value = label_value
        elif timeout and has_solution:
            report_value = label_value

    if timeout:
        report_time = 600.0
        report_time_rule = "runlim_timeout_cap"
    elif total_time is not None:
        report_time = total_time
        report_time_rule = "python_total_time"
    elif infeasible and time_taken is not None:
        report_time = time_taken
        report_time_rule = "python_early_exit_time_taken"
    else:
        report_time = None
        report_time_rule = "missing"

    if timeout:
        time_taken_role = "intermediate_before_runlim_timeout"
    elif infeasible and time_taken is not None:
        time_taken_role = "early_exit"
    elif time_taken is not None:
        time_taken_role = "intermediate_or_final_unsat_step"
    else:
        time_taken_role = ""

    return {
        "source_family": "current",
        "method": method,
        "variant": variant,
        "preprocessing": "on" if preprocessing else "off",
        "dataset": log_path.stem,
        "status": status,
        "report_value": report_value,
        "report_time_s": report_time,
        "report_time_rule": report_time_rule,
        "python_e2e_time_s": total_time if total_time is not None else (time_taken if infeasible else None),
        "time_taken_s": time_taken,
        "total_time_s": total_time,
        "time_taken_role": time_taken_role,
        "timeout_limit_s": 600.0 if timeout else None,
        "log_path": str(log_path),
    }


def parse_legacy_log(
    log_path: Path,
    preprocessing: bool,
    method: str,
    variant: str,
    source_family: str,
) -> dict[str, object]:
    text = log_path.read_text(encoding="utf-8", errors="ignore")

    timeout = has_runlim_timeout(text)
    oom = has_runlim_oom(text)

    value = last_incumbent_label_value(text)
    if value is None and method == "CPX_CP":
        value = parse_cplex_cp_objective(text)
    total_time_candidates = [
        last_float(LEGACY_TOTAL_TIME_USED_RE, text),
        last_float(CP_TOTAL_TIME_RE, text),
        last_float(CARD_TOTAL_TIME_RE, text),
        last_float(TIME_TAKEN_RE, text),
    ]
    raw_last_time = next((value_ for value_ in total_time_candidates if value_ is not None), None)

    if timeout:
        status = "TO"
    elif oom:
        status = "MO"
    elif value is not None:
        status = "OPT"
    else:
        status = "INF"

    if timeout:
        report_time = 600.0
        report_time_rule = "legacy_timeout_cap"
    else:
        report_time = raw_last_time
        report_time_rule = "legacy_last_total_or_time_taken"

    return {
        "source_family": source_family,
        "method": method,
        "variant": variant,
        "preprocessing": "on" if preprocessing else "off",
        "dataset": log_path.stem,
        "status": status,
        "report_value": value if value is not None else "-",
        "report_time_s": report_time,
        "report_time_rule": report_time_rule,
        "python_e2e_time_s": raw_last_time if not timeout else None,
        "time_taken_s": last_float(TIME_TAKEN_RE, text),
        "total_time_s": next(
            (value_ for value_ in [
                last_float(LEGACY_TOTAL_TIME_USED_RE, text),
                last_float(CP_TOTAL_TIME_RE, text),
                last_float(CARD_TOTAL_TIME_RE, text),
            ] if value_ is not None),
            None,
        ),
        "time_taken_role": "legacy_last_time_line" if raw_last_time is not None else "",
        "timeout_limit_s": 600.0 if timeout else None,
        "log_path": str(log_path),
    }


def parse_maxsat_rc2_log(log_path: Path, preprocessing: bool, variant: str) -> dict[str, object]:
    text = log_path.read_text(encoding="utf-8", errors="ignore")

    timeout = has_runlim_timeout(text)
    oom = has_runlim_oom(text)
    has_solution = "Found solution!" in text
    has_no_solution = any(
        message in text
        for message in (
            "No solution found.",
            "No solution found in the preprocessing step!",
            "Cannot find solution!",
        )
    )

    if timeout:
        status = "timeout"
    elif oom:
        status = "out_of_memory"
    elif has_solution:
        status = "optimal"
    elif has_no_solution:
        status = "infeasible"
    else:
        status = "unknown"

    time_taken = last_float(TIME_TAKEN_RE, text)
    runlim_real = last_float(RUNLIM_REAL_RE, text)
    label_value = last_incumbent_label_value(text)

    report_value = label_value if label_value is not None and not oom and status in {"optimal", "timeout"} else None
    if timeout:
        report_time = 600.0
        report_time_rule = "runlim_timeout_cap"
    elif time_taken is not None:
        report_time = time_taken
        report_time_rule = "python_time_taken"
    elif status == "infeasible" and runlim_real is not None:
        report_time = runlim_real
        report_time_rule = "runlim_real_for_early_exit"
    else:
        report_time = None
        report_time_rule = "missing"

    if time_taken is not None:
        time_taken_role = "python_final_time_taken"
    elif status == "infeasible" and runlim_real is not None:
        time_taken_role = "runlim_real_for_early_exit"
    else:
        time_taken_role = ""

    return {
        "source_family": "current",
        "method": "maxsat_rc2",
        "variant": variant,
        "preprocessing": "on" if preprocessing else "off",
        "dataset": log_path.stem,
        "status": status,
        "report_value": report_value,
        "report_time_s": report_time,
        "report_time_rule": report_time_rule,
        "python_e2e_time_s": report_time if not timeout else None,
        "time_taken_s": time_taken,
        "total_time_s": runlim_real if time_taken is None else None,
        "time_taken_role": time_taken_role,
        "timeout_limit_s": 600.0 if timeout else None,
        "log_path": str(log_path),
    }


def parse_evalmaxsat_log(log_path: Path, preprocessing: bool, variant: str) -> dict[str, object]:
    text = log_path.read_text(encoding="utf-8", errors="ignore")

    timeout = has_runlim_timeout(text)
    oom = has_runlim_oom(text)
    solver_status_match = EVALMAXSAT_STATUS_RE.findall(text)
    info_status_match = EVALMAXSAT_INFO_STATUS_RE.findall(text)
    solver_status = solver_status_match[-1].strip() if solver_status_match else ""
    info_status = info_status_match[-1].strip() if info_status_match else ""
    solver_total_time = last_float(EVALMAXSAT_TOTAL_TIME_RE, text)
    time_taken = last_float(TIME_TAKEN_RE, text)
    objective = last_int([EVALMAXSAT_INFO_LABELS_RE, EVALMAXSAT_INFO_OBJECTIVE_RE, EVALMAXSAT_OBJECTIVE_RE], text)
    status_text = info_status or solver_status

    if timeout:
        status = "timeout"
    elif oom:
        status = "out_of_memory"
    elif status_text == "OPTIMUM FOUND":
        status = "optimal"
    elif status_text == "UNSATISFIABLE":
        status = "infeasible"
    else:
        status = "unknown"

    report_value = objective if objective is not None and not oom and status in {"optimal", "timeout"} else None
    if timeout:
        report_time = 600.0
        report_time_rule = "runlim_timeout_cap"
    elif time_taken is not None:
        report_time = time_taken
        report_time_rule = "python_time_taken"
    elif solver_total_time is not None:
        report_time = solver_total_time
        report_time_rule = "evalmaxsat_solver_total_time"
    else:
        report_time = None
        report_time_rule = "missing"

    return {
        "source_family": "current",
        "method": "evalmaxsat",
        "variant": variant,
        "preprocessing": "on" if preprocessing else "off",
        "dataset": log_path.stem,
        "status": status,
        "report_value": report_value,
        "report_time_s": report_time,
        "report_time_rule": report_time_rule,
        "python_e2e_time_s": time_taken if not timeout else None,
        "time_taken_s": time_taken,
        "total_time_s": solver_total_time,
        "time_taken_role": "python_final_time_taken" if time_taken is not None else "evalmaxsat_solver_total_time",
        "timeout_limit_s": 600.0 if timeout else None,
        "log_path": str(log_path),
    }


def collect_cpsat_rows(source_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    configs = [
        (source_root / "CPSAT" / "results", "cpsat", "mip_style"),
        (source_root / "CPSAT_CP" / "results", "cpsat_cp", "cp_style"),
    ]
    for root, method, variant in configs:
        for mode_name, preprocessing in (("preprocessing", True), ("no_preprocessing", False)):
            mode_dir = root / mode_name
            if not mode_dir.exists():
                continue
            for log_path in sorted(mode_dir.glob("*.log")):
                rows.append(parse_cpsat_log(log_path, preprocessing, method, variant))

    return rows


def collect_cardinality_rows(source_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    pairwise_root = source_root / "SAT" / "pairwise" / "results"
    for mode_name, preprocessing in (("preprocessing", True), ("no_preprocessing", False)):
        mode_dir = pairwise_root / mode_name
        if not mode_dir.exists():
            continue
        for variant_dir in sorted(mode_dir.iterdir()):
            if not variant_dir.is_dir():
                continue
            if variant_dir.name.startswith("matched_"):
                method = "cardinality"
                variant = variant_dir.name.removeprefix("matched_").lower()
            elif variant_dir.name in {"dse_inc", "dse_incsc"}:
                method = "sat_pairwise"
                variant = variant_dir.name.lower()
            else:
                continue
            for log_path in sorted(variant_dir.glob("*.log")):
                rows.append(parse_cardinality_log(log_path, preprocessing, variant, method))
    return rows


def collect_legacy_rows(source_root: Path, family_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    legacy_root = source_root / ("Result2" if family_name == "legacy_result2" else "Result")

    if family_name == "legacy_result2":
        configs = [
            (
                legacy_root / "pre_processing" / "SAT" / "PSE" / "preprocessing" / "nsc_assumptions",
                True,
                "POSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "SAT" / "PSE" / "preprocessing" / "tot_assumptions",
                True,
                "POSE_INC",
                "tot_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "SAT" / "pairwise" / "preprocessing" / "nsc_assumptions",
                True,
                "DSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "Gurobi" / "pre_processing",
                True,
                "GUR",
                "gurobi",
            ),
            (
                legacy_root / "pre_processing" / "CPLEX" / "CP" / "preprocessing",
                True,
                "CPX_CP",
                "cp",
            ),
            (
                legacy_root / "pre_processing" / "CPLEX" / "MIP" / "preprocessing",
                True,
                "CPX_MP",
                "mip",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "PSE" / "no_preprocessing" / "nsc_assumptions",
                False,
                "POSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "PSE" / "no_preprocessing" / "tot_assumptions",
                False,
                "POSE_INC",
                "tot_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "pairwise" / "no_pre_processing" / "nsc_assumptions",
                False,
                "DSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "Gurobi" / "no_pre_processing",
                False,
                "GUR",
                "gurobi",
            ),
            (
                legacy_root / "no_pre_processing" / "CPLEX" / "CP" / "no_preprocessing",
                False,
                "CPX_CP",
                "cp",
            ),
            (
                legacy_root / "no_pre_processing" / "CPLEX" / "MIP" / "no_preprocessing",
                False,
                "CPX_MP",
                "mip",
            ),
        ]
    else:
        configs = [
            (
                legacy_root / "pre_processing" / "SAT" / "PSE" / "nsc_assumptions",
                True,
                "POSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "SAT" / "PSE" / "tot_assumptions",
                True,
                "POSE_INC",
                "tot_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "SAT" / "Pairwise" / "nsc_assumptions",
                True,
                "DSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "pre_processing" / "Gurobi" / "results",
                True,
                "GUR",
                "gurobi",
            ),
            (
                legacy_root / "pre_processing" / "CPLEX" / "CP" / "results",
                True,
                "CPX_CP",
                "cp",
            ),
            (
                legacy_root / "pre_processing" / "CPLEX" / "MIP" / "result",
                True,
                "CPX_MP",
                "mip",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "PSE" / "nsc_assumptions",
                False,
                "POSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "PSE" / "tot_assumptions",
                False,
                "POSE_INC",
                "tot_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "SAT" / "Pairwise" / "nsc_assumptions",
                False,
                "DSE_INCSC",
                "nsc_assumptions",
            ),
            (
                legacy_root / "no_pre_processing" / "Gurobi" / "results",
                False,
                "GUR",
                "gurobi",
            ),
            (
                legacy_root / "no_pre_processing" / "CPLEX" / "CP" / "results",
                False,
                "CPX_CP",
                "cp",
            ),
            (
                legacy_root / "no_pre_processing" / "CPLEX" / "MIP" / "results",
                False,
                "CPX_MP",
                "mip",
            ),
        ]

    for log_dir, preprocessing, method, variant in configs:
        if not log_dir.exists():
            continue
        for log_path in sorted(log_dir.glob("*.log")):
            rows.append(parse_legacy_log(log_path, preprocessing, method, variant, family_name))

    return rows


def collect_maxsat_rc2_rows(source_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    maxsat_root = source_root / "MaxSAT" / "results"

    pose_configs = [
        (maxsat_root / "processing" / "POSE", True, "pose"),
        (maxsat_root / "no_processing" / "POSE", False, "pose"),
    ]
    for log_dir, preprocessing, variant in pose_configs:
        if not log_dir.exists():
            continue
        for log_path in sorted(log_dir.glob("*.log")):
            rows.append(parse_maxsat_rc2_log(log_path, preprocessing, variant))

    for mode_name, preprocessing in (("processing", True), ("no_processing", False)):
        dse_root = maxsat_root / mode_name / "DSE"
        if not dse_root.exists():
            continue
        for log_path in sorted(dse_root.glob("*.log")):
            rows.append(parse_maxsat_rc2_log(log_path, preprocessing, "dse"))
        for variant_dir in sorted(dse_root.iterdir()):
            if not variant_dir.is_dir():
                continue
            variant = f"dse_{variant_dir.name.lower()}"
            for log_path in sorted(variant_dir.glob("*.log")):
                rows.append(parse_maxsat_rc2_log(log_path, preprocessing, variant))

    for mode_name, preprocessing in (("processing", True), ("no_processing", False)):
        mode_dir = maxsat_root / mode_name
        if not mode_dir.exists():
            continue
        for variant_dir in sorted(mode_dir.glob("CARD_*")):
            if not variant_dir.is_dir():
                continue
            variant = variant_dir.name.lower()
            for log_path in sorted(variant_dir.glob("*.log")):
                rows.append(parse_maxsat_rc2_log(log_path, preprocessing, variant))

    return rows


def collect_evalmaxsat_rows(source_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    eval_root = source_root / "evalmaxsat" / "results"
    configs = [
        (eval_root / "processing" / "pipeline", True),
        (eval_root / "no_preprocessing" / "pipeline", False),
    ]

    for pipeline_root, preprocessing in configs:
        if not pipeline_root.exists():
            continue
        for variant_dir in sorted(pipeline_root.iterdir()):
            if not variant_dir.is_dir():
                continue
            variant = variant_dir.name.lower()
            for log_path in sorted(variant_dir.glob("*.log")):
                rows.append(parse_evalmaxsat_log(log_path, preprocessing, variant))

    return rows


def write_csv(rows: list[dict[str, object]], output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_family",
        "method",
        "variant",
        "preprocessing",
        "dataset",
        "status",
        "report_value",
        "report_time_s",
        "report_time_rule",
        "python_e2e_time_s",
        "time_taken_s",
        "total_time_s",
        "time_taken_role",
        "timeout_limit_s",
        "log_path",
    ]
    with output_csv.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    tools_dir = Path(__file__).resolve().parent
    stats_dir = tools_dir.parent
    source_root = stats_dir.parent
    default_output = stats_dir / "python_total_times_all_methods.csv"

    parser = argparse.ArgumentParser(
        description="Extract normalized report times and statuses from current and legacy MO-FAP logs."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=source_root,
        help="Path to the SourceCode directory.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=default_output,
        help="Output CSV path.",
    )
    parser.add_argument(
        "--skip-legacy-result2",
        action="store_true",
        help="Skip extraction from SourceCode/Result2 legacy logs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_root = args.source_root.resolve()

    rows: list[dict[str, object]] = []
    rows.extend(collect_cpsat_rows(source_root))
    rows.extend(collect_cardinality_rows(source_root))
    rows.extend(collect_maxsat_rc2_rows(source_root))
    rows.extend(collect_evalmaxsat_rows(source_root))
    if not args.skip_legacy_result2:
        rows.extend(collect_legacy_rows(source_root, "legacy_result2"))
        rows.extend(collect_legacy_rows(source_root, "legacy_result"))

    rows.sort(
        key=lambda row: (
            str(row["source_family"]),
            str(row["method"]),
            str(row["variant"]),
            str(row["preprocessing"]),
            dataset_sort_key(str(row["dataset"])),
        )
    )

    output_csv = args.output_csv.resolve()
    write_csv(rows, output_csv)
    print(f"Wrote {len(rows)} rows to {output_csv}")


if __name__ == "__main__":
    main()

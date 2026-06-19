import argparse
import contextlib
import csv
import importlib.util
import io
import os
import re
import shlex
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


ARG_LINE_RE = re.compile(r"^\[runlim\]\s+argv\[(\d+)\]:\s+(.*)$")
TRYING_RE = re.compile(r"Trying with at most\s+(\d+)\s+labels")
OPTIMAL_RE = re.compile(r"Optimal number of labels used:\s+(\d+)")


@dataclass
class LogConfig:
    log_path: Path
    script_name: str
    dataset: str
    type_sat: str
    type_card: int
    distance_mode: str
    distance_card: int
    target_bound: int
    status: str
    target_source: str


@dataclass
class StatsRow:
    log_path: str
    script_name: str
    dataset: str
    type_sat: str
    type_card: int
    distance_mode: str
    distance_card: int
    target_bound: int
    status: str
    target_source: str
    preprocessed: bool
    base_vars: int
    base_clauses: int
    label_vars: int
    label_clauses: int
    bound_vars: int
    bound_clauses: int
    total_vars: int
    total_clauses: int


class CountingSolver:
    def __init__(self) -> None:
        self._max_var = 0
        self._num_clauses = 0

    def add_clause(self, clause: List[int]) -> None:
        self._num_clauses += 1
        if clause:
            self._max_var = max(self._max_var, max(abs(lit) for lit in clause))

    def nof_vars(self) -> int:
        return self._max_var

    def nof_clauses(self) -> int:
        return self._num_clauses

    def delete(self) -> None:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild pairwise SAT formulas from old logs and extract variable/clause counts."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Log files or directories containing .log files.",
    )
    parser.add_argument(
        "--output",
        help="Optional CSV output path.",
    )
    return parser.parse_args()


def iter_log_files(inputs: Iterable[str]) -> List[Path]:
    logs: List[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_file() and path.suffix.lower() == ".log":
            logs.append(path)
        elif path.is_dir():
            logs.extend(sorted(path.rglob("*.log")))
        else:
            raise FileNotFoundError(f"Unsupported input path: {path}")
    if not logs:
        raise FileNotFoundError("No .log files found in the given inputs.")
    return logs


def parse_runlim_argv(lines: List[str]) -> Optional[List[str]]:
    argv_map = {}
    for line in lines:
        match = ARG_LINE_RE.match(line.strip())
        if match:
            argv_map[int(match.group(1))] = match.group(2).strip()
    if not argv_map:
        return None
    max_idx = max(argv_map)
    return [argv_map[idx] for idx in range(max_idx + 1) if idx in argv_map]


def parse_command_line(lines: List[str]) -> Optional[List[str]]:
    for line in lines:
        if line.startswith("COMMAND:"):
            return shlex.split(line.split("COMMAND:", 1)[1].strip())
    return None


def extract_command(lines: List[str]) -> List[str]:
    argv = parse_runlim_argv(lines)
    if argv is not None:
        return argv
    command = parse_command_line(lines)
    if command is not None:
        return command
    raise ValueError("Cannot parse command line from log.")


def extract_target_bound(lines: List[str]) -> tuple[int, str, str]:
    optimal_value: Optional[int] = None
    for line in lines:
        match = OPTIMAL_RE.search(line)
        if match:
            optimal_value = int(match.group(1))

    trying_values = [int(match.group(1)) for line in lines for match in [TRYING_RE.search(line)] if match]
    last_trying = trying_values[-1] if trying_values else None

    if optimal_value is not None:
        return optimal_value - 1, "optimal", "optimal_minus_one"
    if last_trying is not None:
        return last_trying, "timeout", "last_trying_line"
    if any("has no valid labels after preprocessing" in line for line in lines):
        return 0, "preprocess_unsat", "no_formula"
    if any("Cannot find solution!" in line for line in lines):
        return 0, "preprocess_unsat", "no_formula"
    if any("Solve first problem:" in line for line in lines) and any("Cannot find solution." in line for line in lines):
        return 0, "first_solve_unsat", "no_trying_line"
    raise ValueError("Cannot infer target bound from log.")


def parse_log_config(log_path: Path) -> LogConfig:
    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    argv = extract_command(lines)

    if len(argv) < 6:
        raise ValueError(f"Unexpected command format in {log_path}")

    script_name = os.path.basename(argv[2])
    dataset = argv[3]
    type_sat = argv[4]
    type_card = int(argv[5])
    distance_mode = argv[6].lower() if len(argv) >= 7 else "pairwise"
    distance_card = int(argv[7]) if len(argv) >= 8 else type_card
    target_bound, status, target_source = extract_target_bound(lines)

    return LogConfig(
        log_path=log_path,
        script_name=script_name,
        dataset=dataset,
        type_sat=type_sat,
        type_card=type_card,
        distance_mode=distance_mode,
        distance_card=distance_card,
        target_bound=target_bound,
        status=status,
        target_source=target_source,
    )


def load_module(script_path: Path):
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    fake_psutil = types.ModuleType("psutil")
    fake_psutil.Process = object
    previous_psutil = sys.modules.get("psutil")
    sys.modules["psutil"] = fake_psutil
    try:
        spec.loader.exec_module(module)
    finally:
        if previous_psutil is None:
            sys.modules.pop("psutil", None)
        else:
            sys.modules["psutil"] = previous_psutil
    return module


def silent_call(func, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


def build_stats(config: LogConfig) -> StatsRow:
    script_dir = Path(__file__).resolve().parent
    script_path = script_dir / config.script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Referenced solver script not found: {script_path}")

    module = load_module(script_path)

    dataset_folder = script_dir / "dataset" / config.dataset
    files = silent_call(module.get_file_names, str(dataset_folder))
    domain = silent_call(module.read_domain, files["domain"])
    var = silent_call(module.read_var, files["var"], domain)

    preprocessed = config.script_name == "pairwise.py"
    if preprocessed:
        ok = silent_call(module.delete_invalid_labels, var, files["ctr"])
        if not ok:
            if config.status == "preprocess_unsat":
                return StatsRow(
                    log_path=str(config.log_path),
                    script_name=config.script_name,
                    dataset=config.dataset,
                    type_sat=config.type_sat,
                    type_card=config.type_card,
                    distance_mode=config.distance_mode,
                    distance_card=config.distance_card,
                    target_bound=config.target_bound,
                    status=config.status,
                    target_source=config.target_source,
                    preprocessed=preprocessed,
                    base_vars=0,
                    base_clauses=0,
                    label_vars=0,
                    label_clauses=0,
                    bound_vars=0,
                    bound_clauses=0,
                    total_vars=0,
                    total_clauses=0,
                )
            raise ValueError(f"Preprocessing removed all labels for at least one variable in {config.log_path}")

    solver = CountingSolver()
    top_id, var_map = silent_call(module.create_var_map, var)
    top_id = silent_call(
        module.build_constraints,
        solver,
        var,
        var_map,
        files["ctr"],
        config.type_card,
        config.distance_mode,
        config.distance_card,
    )
    base_vars = solver.nof_vars()
    base_clauses = solver.nof_clauses()

    if config.status == "first_solve_unsat":
        return StatsRow(
            log_path=str(config.log_path),
            script_name=config.script_name,
            dataset=config.dataset,
            type_sat=config.type_sat,
            type_card=config.type_card,
            distance_mode=config.distance_mode,
            distance_card=config.distance_card,
            target_bound=config.target_bound,
            status=config.status,
            target_source=config.target_source,
            preprocessed=preprocessed,
            base_vars=base_vars,
            base_clauses=base_clauses,
            label_vars=0,
            label_clauses=0,
            bound_vars=0,
            bound_clauses=0,
            total_vars=base_vars,
            total_clauses=base_clauses,
        )

    label_var_map = silent_call(module.create_label_var_map, domain[0], top_id + 1)
    silent_call(module.build_label_constraints, solver, var_map, label_var_map)
    after_label_vars = solver.nof_vars()
    after_label_clauses = solver.nof_clauses()

    silent_call(module.add_limit_label_constraints, solver, label_var_map, config.target_bound)
    total_vars = solver.nof_vars()
    total_clauses = solver.nof_clauses()

    return StatsRow(
        log_path=str(config.log_path),
        script_name=config.script_name,
        dataset=config.dataset,
        type_sat=config.type_sat,
        type_card=config.type_card,
        distance_mode=config.distance_mode,
        distance_card=config.distance_card,
        target_bound=config.target_bound,
        status=config.status,
        target_source=config.target_source,
        preprocessed=preprocessed,
        base_vars=base_vars,
        base_clauses=base_clauses,
        label_vars=after_label_vars - base_vars,
        label_clauses=after_label_clauses - base_clauses,
        bound_vars=total_vars - after_label_vars,
        bound_clauses=total_clauses - after_label_clauses,
        total_vars=total_vars,
        total_clauses=total_clauses,
    )


def write_csv(rows: List[StatsRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(rows[0].__dict__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def print_summary(rows: List[StatsRow]) -> None:
    for row in rows:
        print(
            f"{row.dataset}: bound={row.target_bound}, vars={row.total_vars}, clauses={row.total_clauses}, "
            f"base=({row.base_vars},{row.base_clauses}), label=({row.label_vars},{row.label_clauses}), "
            f"bound_part=({row.bound_vars},{row.bound_clauses}), log={row.log_path}"
        )


def main() -> None:
    args = parse_args()
    log_files = iter_log_files(args.inputs)
    rows = [build_stats(parse_log_config(log_path)) for log_path in log_files]
    print_summary(rows)
    if args.output:
        write_csv(rows, Path(args.output))


if __name__ == "__main__":
    main()

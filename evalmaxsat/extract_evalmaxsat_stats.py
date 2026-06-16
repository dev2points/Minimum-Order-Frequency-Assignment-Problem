import argparse
import contextlib
import csv
import importlib.util
import io
import os
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from pysat.formula import WCNF


ARG_LINE_RE = re.compile(r"^\[runlim\]\s+argv\[(\d+)\]:\s+(.*)$")


@dataclass
class LogConfig:
    log_path: Path
    script_name: str
    dataset: str
    encoding: str
    card_encoding: Optional[int]
    preprocessed: bool
    decode_path: Path


@dataclass
class StatsRow:
    log_path: str
    script_name: str
    dataset: str
    encoding: str
    card_encoding: Optional[int]
    preprocessed: bool
    status: str
    decode_exists: bool
    solver_status: Optional[str]
    objective: Optional[int]
    decision_vars: int
    order_vars: int
    card_aux_vars: int
    label_vars: int
    total_vars: int
    order_clauses: int
    card_clauses: int
    distance_clauses: int
    label_link_clauses: int
    soft_clauses: int
    hard_clauses: int
    total_clauses: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild evalmaxsat WCNF formulas from old logs and extract stats."
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


def parse_log_config(log_path: Path) -> LogConfig:
    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    argv = extract_command(lines)

    if len(argv) < 5:
        raise ValueError(f"Unexpected command format in {log_path}")

    script_name = os.path.basename(argv[2])
    if script_name not in {"evalmaxsat_no_processing.py", "evalmaxsat.py"}:
        raise ValueError(f"Unsupported evalmaxsat script {script_name} in {log_path}")

    dataset = argv[3]
    encoding = argv[4].upper()
    card_encoding = int(argv[5]) if len(argv) >= 6 and encoding == "DSE" else None
    preprocessed = script_name == "evalmaxsat.py"

    group = "POSE" if encoding == "POSE" else f"DSE_{card_encoding}"
    decode_path = (
        Path(__file__).resolve().parent
        / "results"
        / ("processing" if preprocessed else "no_preprocessing")
        / "decode"
        / group
        / f"{dataset}.decoded.txt"
    )

    return LogConfig(
        log_path=log_path,
        script_name=script_name,
        dataset=dataset,
        encoding=encoding,
        card_encoding=card_encoding,
        preprocessed=preprocessed,
        decode_path=decode_path,
    )


def load_module(script_path: Path):
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def silent_call(func, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


def parse_decode_file(decode_path: Path) -> tuple[bool, Optional[str], Optional[int]]:
    if not decode_path.exists():
        return False, None, None

    solver_status = None
    objective = None
    for line in decode_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("solver_status="):
            solver_status = line.split("=", 1)[1].strip() or None
        elif line.startswith("objective="):
            raw = line.split("=", 1)[1].strip()
            if raw and raw != "None":
                objective = int(raw)
    return True, solver_status, objective


def has_generation_error(log_path: Path) -> bool:
    for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "[ERROR] Generation failed:" in line:
            return True
    return False


def build_stats(config: LogConfig) -> StatsRow:
    if has_generation_error(config.log_path):
        decode_exists, solver_status, objective = parse_decode_file(config.decode_path)
        return StatsRow(
            log_path=str(config.log_path),
            script_name=config.script_name,
            dataset=config.dataset,
            encoding=config.encoding,
            card_encoding=config.card_encoding,
            preprocessed=config.preprocessed,
            status="generation_error",
            decode_exists=decode_exists,
            solver_status=solver_status,
            objective=objective,
            decision_vars=0,
            order_vars=0,
            card_aux_vars=0,
            label_vars=0,
            total_vars=0,
            order_clauses=0,
            card_clauses=0,
            distance_clauses=0,
            label_link_clauses=0,
            soft_clauses=0,
            hard_clauses=0,
            total_clauses=0,
        )

    script_dir = Path(__file__).resolve().parent
    script_path = script_dir / config.script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Referenced solver script not found: {script_path}")

    module = load_module(script_path)

    dataset_folder = script_dir / "dataset" / config.dataset
    files = silent_call(module.get_file_names, str(dataset_folder))
    domain = silent_call(module.read_domain, files["domain"])
    var = silent_call(module.read_var, files["var"], domain)

    if config.preprocessed:
        ok = silent_call(module.delete_invalid_labels, var, files["ctr"])
        if not ok:
            decode_exists, solver_status, objective = parse_decode_file(config.decode_path)
            return StatsRow(
                log_path=str(config.log_path),
                script_name=config.script_name,
                dataset=config.dataset,
                encoding=config.encoding,
                card_encoding=config.card_encoding,
                preprocessed=True,
                status="preprocess_unsat",
                decode_exists=decode_exists,
                solver_status=solver_status,
                objective=objective,
                decision_vars=0,
                order_vars=0,
                card_aux_vars=0,
                label_vars=0,
                total_vars=0,
                order_clauses=0,
                card_clauses=0,
                distance_clauses=0,
                label_link_clauses=0,
                soft_clauses=0,
                hard_clauses=0,
                total_clauses=0,
            )

    last_var_num, var_map = silent_call(module.create_var_map, var)
    wcnf = WCNF()
    stats = {
        "decision_vars": len(var_map),
        "order_vars": 0,
        "card_aux_vars": 0,
        "label_vars": 0,
        "order_clauses": 0,
        "card_clauses": 0,
        "distance_clauses": 0,
        "label_link_clauses": 0,
        "soft_clauses": 0,
    }

    if config.encoding == "POSE":
        top_var_num = silent_call(
            module.build_constraints_pose,
            wcnf,
            var,
            var_map,
            last_var_num,
            files["ctr"],
            stats,
        )
    elif config.encoding == "DSE":
        if config.card_encoding is None:
            raise ValueError(f"Missing DSE card encoding in {config.log_path}")
        top_var_num = silent_call(
            module.build_constraints_dse,
            wcnf,
            var,
            var_map,
            files["ctr"],
            config.card_encoding,
            stats,
        )
    else:
        raise ValueError(f"Unsupported encoding: {config.encoding}")

    label_var_map = silent_call(module.create_label_var_map, domain[0], top_var_num + 1)
    silent_call(module.build_maxsat_label_constraints, wcnf, var_map, label_var_map, stats)

    decode_exists, solver_status, objective = parse_decode_file(config.decode_path)

    return StatsRow(
        log_path=str(config.log_path),
        script_name=config.script_name,
        dataset=config.dataset,
        encoding=config.encoding,
        card_encoding=config.card_encoding,
        preprocessed=config.preprocessed,
        status="ok",
        decode_exists=decode_exists,
        solver_status=solver_status,
        objective=objective,
        decision_vars=stats["decision_vars"],
        order_vars=stats["order_vars"],
        card_aux_vars=stats["card_aux_vars"],
        label_vars=stats["label_vars"],
        total_vars=wcnf.nv,
        order_clauses=stats["order_clauses"],
        card_clauses=stats["card_clauses"],
        distance_clauses=stats["distance_clauses"],
        label_link_clauses=stats["label_link_clauses"],
        soft_clauses=stats["soft_clauses"],
        hard_clauses=len(wcnf.hard),
        total_clauses=len(wcnf.hard) + len(wcnf.soft),
    )


def write_csv(rows: List[StatsRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(StatsRow.__dataclass_fields__.keys())
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def print_row(row: StatsRow) -> None:
    print(
        f"{Path(row.log_path).name}: vars={row.total_vars}, "
        f"hard={row.hard_clauses}, soft={row.soft_clauses}, total={row.total_clauses}, "
        f"decision={row.decision_vars}, order={row.order_vars}, "
        f"card_aux={row.card_aux_vars}, label={row.label_vars}, "
        f"solver_status={row.solver_status}, objective={row.objective}"
    )


def main() -> None:
    args = parse_args()
    log_files = iter_log_files(args.inputs)
    rows = [build_stats(parse_log_config(log_path)) for log_path in log_files]
    for row in rows:
        print_row(row)
    if args.output:
        write_csv(rows, Path(args.output))


if __name__ == "__main__":
    main()

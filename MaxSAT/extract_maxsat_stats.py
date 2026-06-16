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


@dataclass
class LogConfig:
    log_path: Path
    script_name: str
    dataset: str
    encoding: str
    card_encoding: Optional[int]
    preprocessed: bool


@dataclass
class StatsRow:
    log_path: str
    script_name: str
    dataset: str
    encoding: str
    card_encoding: Optional[int]
    preprocessed: bool
    status: str
    decision_vars: int
    order_vars: int
    card_aux_vars: int
    label_vars: int
    num_vars: int
    order_clauses: int
    card_clauses: int
    distance_clauses: int
    label_link_clauses: int
    soft_clauses: int
    hard_clauses: int
    total_clauses: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild MaxSAT formulas from old logs and extract variable/clause counts."
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
    dataset = argv[3]
    encoding = argv[4].upper()
    card_encoding = int(argv[5]) if len(argv) >= 6 and encoding == "DSE" else None

    return LogConfig(
        log_path=log_path,
        script_name=script_name,
        dataset=dataset,
        encoding=encoding,
        card_encoding=card_encoding,
        preprocessed=script_name == "main.py",
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

    if config.preprocessed:
        ok = silent_call(module.delete_invalid_labels, var, files["ctr"])
        if not ok:
            return StatsRow(
                log_path=str(config.log_path),
                script_name=config.script_name,
                dataset=config.dataset,
                encoding=config.encoding,
                card_encoding=config.card_encoding,
                preprocessed=config.preprocessed,
                status="preprocess_unsat",
                decision_vars=0,
                order_vars=0,
                card_aux_vars=0,
                label_vars=0,
                num_vars=0,
                order_clauses=0,
                card_clauses=0,
                distance_clauses=0,
                label_link_clauses=0,
                soft_clauses=0,
                hard_clauses=0,
                total_clauses=0,
            )

    last_var_num, var_map = silent_call(module.create_var_map, var)
    wcnf = module.WCNF()

    decision_vars = len(var_map)
    order_vars = 0
    card_aux_vars = 0
    card_clauses = 0
    order_clauses = 0

    if config.encoding == "POSE":
        top_var_num = silent_call(module.build_constraints_POSE, wcnf, var, var_map, last_var_num, files["ctr"])
        order_vars = top_var_num - last_var_num
        order_clauses = sum(2 for vals in var.values() if len(vals) >= 1)
        order_clauses += sum(max(len(vals) - 1, 0) for vals in var.values())
        order_clauses += sum(3 * max(len(vals) - 1, 0) for vals in var.values())
    elif config.encoding == "DSE":
        type_card = 1 if config.card_encoding is None else config.card_encoding
        top_var_num = silent_call(module.build_constraints_DSE, wcnf, var, var_map, files["ctr"], type_card)
        card_aux_vars = top_var_num - max(var_map.values())
    else:
        raise ValueError(f"Unsupported encoding: {config.encoding}")

    hard_after_core = len(wcnf.hard)
    label_var_map = silent_call(module.create_label_var_map, domain[0], top_var_num + 1)
    silent_call(module.build_maxsat_label_constraints, wcnf, var_map, label_var_map)

    hard_clauses = len(wcnf.hard)
    soft_clauses = len(wcnf.soft)
    total_clauses = hard_clauses + soft_clauses
    label_vars = len(label_var_map)
    label_link_clauses = len(var_map)
    distance_plus_card_or_order = hard_after_core
    distance_clauses = distance_plus_card_or_order - card_clauses - order_clauses

    if config.encoding == "DSE":
        distance_clauses = 0
        for line in Path(files["ctr"]).read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip() == "\x00":
                continue
            parts = line.strip().split()
            if not parts:
                continue
            i, j = int(parts[0]), int(parts[1])
            vals_i = var.get(i, [])
            vals_j = var.get(j, [])
            if ">" in parts:
                target = int(parts[4])
                for vi in vals_i:
                    for vj in vals_j:
                        if abs(vi - vj) <= target:
                            distance_clauses += 1
            elif "=" in parts:
                distance_clauses += len(vals_i)
        card_clauses = hard_after_core - distance_clauses

    status = "ok"
    if hard_clauses == 0 and soft_clauses == 0:
        status = "empty"

    return StatsRow(
        log_path=str(config.log_path),
        script_name=config.script_name,
        dataset=config.dataset,
        encoding=config.encoding,
        card_encoding=config.card_encoding,
        preprocessed=config.preprocessed,
        status=status,
        decision_vars=decision_vars,
        order_vars=order_vars,
        card_aux_vars=card_aux_vars,
        label_vars=label_vars,
        num_vars=wcnf.nv,
        order_clauses=order_clauses,
        card_clauses=card_clauses,
        distance_clauses=distance_clauses,
        label_link_clauses=label_link_clauses,
        soft_clauses=soft_clauses,
        hard_clauses=hard_clauses,
        total_clauses=total_clauses,
    )


def write_csv(rows: List[StatsRow], output_path: Path) -> None:
    fieldnames = list(StatsRow.__dataclass_fields__.keys())
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def print_row(row: StatsRow) -> None:
    print(
        f"{Path(row.log_path).name}: vars={row.num_vars}, "
        f"hard={row.hard_clauses}, soft={row.soft_clauses}, total={row.total_clauses}, "
        f"decision={row.decision_vars}, order={row.order_vars}, "
        f"card_aux={row.card_aux_vars}, label={row.label_vars}"
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

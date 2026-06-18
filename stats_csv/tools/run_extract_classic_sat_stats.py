#!/usr/bin/env python3
import argparse
import csv
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pairwise and sequence SAT extractors, then build a merged classic-SAT CSV."
    )
    parser.add_argument(
        "--python-exe",
        default=sys.executable,
        help="Python interpreter used to run the extractor scripts. Defaults to the current interpreter.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Directory for generated CSV files. Defaults to SourceCode/stats_csv/generated_comparison.",
    )
    return parser.parse_args()


def run_command(cmd: list[str]) -> None:
    print("Running:", " ".join(str(part) for part in cmd))
    subprocess.run(cmd, check=True)


def pairwise_input_dirs(pairwise_dir: Path) -> list[Path]:
    results_dir = pairwise_dir / "results"
    if not results_dir.exists():
        raise FileNotFoundError(f"Results directory not found: {results_dir}")
    return sorted(path for path in results_dir.iterdir() if path.is_dir())


def sequence_input_dirs(sequence_dir: Path, source_code_dir: Path) -> list[Path]:
    candidate_dirs = [
        source_code_dir / "Result_python" / "no_pre_processing" / "SAT" / "PSE",
        source_code_dir / "Result_python" / "pre_processing" / "SAT" / "PSE",
        sequence_dir / "results" / "preprocessing",
    ]
    existing = [path for path in candidate_dirs if path.exists()]
    if not existing:
        raise FileNotFoundError("No sequence log directories found.")
    return existing


def read_csv_rows(path: Path, source_family: str) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = []
        for row in reader:
            row = dict(row)
            row["source_family"] = source_family
            rows.append(row)
        return rows


def write_merged_csv(rows: Iterable[dict[str, str]], output_path: Path) -> None:
    rows = list(rows)
    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()

    tools_dir = Path(__file__).resolve().parent
    stats_csv_dir = tools_dir.parent
    source_code_dir = stats_csv_dir.parent
    pairwise_dir = source_code_dir / "SAT" / "pairwise"
    sequence_dir = source_code_dir / "SAT" / "sequence"

    output_dir = Path(args.output_dir) if args.output_dir else (stats_csv_dir / "generated_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)

    pairwise_extractor = pairwise_dir / "extract_pairwise_stats.py"
    sequence_extractor = sequence_dir / "extract_sequence_stats.py"
    pairwise_csv = output_dir / "pairwise_stats_all.csv"
    sequence_csv = output_dir / "sequence_stats_all.csv"
    merged_csv = output_dir / "classic_sat_stats_all.csv"

    for required in (pairwise_extractor, sequence_extractor):
        if not required.exists():
            raise FileNotFoundError(f"Extractor not found: {required}")

    pairwise_inputs = pairwise_input_dirs(pairwise_dir)
    sequence_inputs = sequence_input_dirs(sequence_dir, source_code_dir)

    print(f"Using Python: {args.python_exe}")
    print(f"Output directory: {output_dir}")
    print("Pairwise inputs:")
    for path in pairwise_inputs:
        print(f"  - {path}")
    print("Sequence inputs:")
    for path in sequence_inputs:
        print(f"  - {path}")

    run_command(
        [args.python_exe, str(pairwise_extractor), *[str(path) for path in pairwise_inputs], "--output", str(pairwise_csv)]
    )
    run_command(
        [args.python_exe, str(sequence_extractor), *[str(path) for path in sequence_inputs], "--output", str(sequence_csv)]
    )

    merged_rows = []
    merged_rows.extend(read_csv_rows(pairwise_csv, "pairwise"))
    merged_rows.extend(read_csv_rows(sequence_csv, "sequence"))
    write_merged_csv(merged_rows, merged_csv)

    print(f"Done. Pairwise CSV: {pairwise_csv}")
    print(f"Done. Sequence CSV: {sequence_csv}")
    print(f"Done. Merged classic SAT CSV: {merged_csv}")


if __name__ == "__main__":
    main()

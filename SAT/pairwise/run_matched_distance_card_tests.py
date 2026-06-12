import argparse
import os
import subprocess
import time
from types import SimpleNamespace

from run_distance_card_tests import (
    ENCODING_NAMES,
    format_encoding,
    normalize_dataset,
    parse_log,
    run_case,
    write_summary,
)


DEFAULT_DATASETS = [
    "scen04",
    "graph03",
    "graph04",
    "graph14",
    "TUD200.1",
    "TUD916.1",
]

DEFAULT_CARDS = [1, 2, 3, 4, 5, 6, 7, 8]


def main():
    parser = argparse.ArgumentParser(
        description="Run matched exactly-one and distance-card tests."
    )
    parser.add_argument(
        "datasets",
        nargs="*",
        help="Datasets or aliases, e.g. g4 g14 t916.1",
    )
    parser.add_argument("--solve-mode", default="assumptions", choices=["first", "assumptions", "incremental"])
    parser.add_argument("--cards", type=int, nargs="+", default=DEFAULT_CARDS)
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per run in seconds.")
    parser.add_argument(
        "--scripts",
        nargs="+",
        default=["pairwise.py"],
        choices=["pairwise.py", "pairwise_no_preprocessing.py"],
        help="Which encoders to run.",
    )
    parser.add_argument("--log-dir", default=os.path.join("results", "distance_card_matched_tests"))
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    datasets = [normalize_dataset(x) for x in (args.datasets or DEFAULT_DATASETS)]
    run_id = time.strftime("run_%Y%m%d_%H%M%S") + f"_{os.getpid()}"
    log_root = os.path.join(script_dir, args.log_dir, run_id)
    os.makedirs(log_root, exist_ok=True)

    print("Datasets:", ", ".join(datasets))
    print("Scripts:", ", ".join(args.scripts))
    print("solve_mode:", args.solve_mode)
    print("matched_cards:", ", ".join(format_encoding(x) for x in args.cards))
    print("distance_mode: card")
    print("timeout:", args.timeout)
    print("log_dir:", log_root)
    print()

    failures = 0
    rows = []
    run_args = SimpleNamespace(
        solve_mode=args.solve_mode,
        distance_mode="card",
        timeout=args.timeout,
    )

    for card in args.cards:
        config = f"eo{card}_dist{card}"
        for script_name in args.scripts:
            group = "processing" if script_name == "pairwise.py" else "no_processing"
            group_dir = os.path.join(log_root, config, group)
            os.makedirs(group_dir, exist_ok=True)

            for dataset in datasets:
                log_path = os.path.join(group_dir, f"{dataset}.log")
                print(f"[RUN] {config} {group} {dataset} -> {log_path}")
                try:
                    returncode, elapsed = run_case(script_dir, script_name, dataset, run_args, card, card, log_path)
                except subprocess.TimeoutExpired:
                    returncode, elapsed = "", args.timeout
                    status = "TIMEOUT"
                    failures += 1
                    with open(log_path, "a", encoding="utf-8", errors="replace") as log:
                        log.write(f"\n[TIMEOUT] exceeded {args.timeout} seconds\n")
                except Exception as exc:
                    returncode, elapsed = "", ""
                    status = "FAIL"
                    failures += 1
                    with open(log_path, "a", encoding="utf-8", errors="replace") as log:
                        log.write(f"\n[ERROR] {exc}\n")
                else:
                    status = "OK" if returncode == 0 else "FAIL"
                    if returncode != 0:
                        failures += 1

                row = {
                    "dataset": dataset,
                    "group": group,
                    "script": script_name,
                    "solve_mode": args.solve_mode,
                    "type_card": card,
                    "type_card_name": ENCODING_NAMES.get(card, "unknown"),
                    "distance_mode": "card",
                    "distance_card": card,
                    "distance_card_name": ENCODING_NAMES.get(card, "unknown"),
                    "status": status,
                    "returncode": returncode,
                    "wall_time_sec": f"{elapsed:.2f}" if isinstance(elapsed, float) else elapsed,
                    "log_path": log_path,
                }
                row.update(parse_log(log_path))
                rows.append(row)
                write_summary(log_root, rows)

                if status == "OK":
                    print(f"[OK] {config} {group} {dataset}: time={elapsed:.2f}s")
                elif status == "TIMEOUT":
                    print(f"[TIMEOUT] {config} {group} {dataset} after {args.timeout}s")
                else:
                    print(f"[FAIL] {config} {group} {dataset}: returncode={returncode}, time={elapsed}")

    print()
    print("summary_csv:", os.path.join(log_root, "summary.csv"))
    print("summary_md:", os.path.join(log_root, "summary.md"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

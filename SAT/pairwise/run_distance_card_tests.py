import argparse
import os
import subprocess
import sys
import time


DEFAULT_DATASETS = [
    "graph04",
]

ALIASES = {
    "g3": "graph03",
    "g03": "graph03",
    "g4": "graph04",
    "g04": "graph04",
    "g11": "graph11",
    "g12": "graph12",
    "g13": "graph13",
    "t2.1": "TUD200.1",
    "t200.1": "TUD200.1",
    "t9.1": "TUD916.1",
    "t916.1": "TUD916.1",
    "t9.3": "TUD916.3",
    "t916.3": "TUD916.3",
}

ENCODING_NAMES = {
    0: "pairwise",
    1: "seqcounter",
    2: "sortnetwrk",
    3: "cardnetwrk",
    4: "bitwise",
    5: "ladder",
    6: "totalizer",
    7: "mtotalizer",
    8: "kmtotalizer",
    9: "native",
}


def normalize_dataset(name):
    return ALIASES.get(name.lower(), name)


def format_encoding(encoding_id):
    return f"{encoding_id} ({ENCODING_NAMES.get(encoding_id, 'unknown')})"


def run_case(script_dir, script_name, dataset, args, type_card, distance_card, log_path):
    cmd = [
        sys.executable,
        "-u",
        script_name,
        dataset,
        args.solve_mode,
        str(type_card),
        args.distance_mode,
        str(distance_card),
    ]

    start = time.perf_counter()
    with open(log_path, "w", encoding="utf-8", errors="replace") as log:
        log.write("COMMAND: " + " ".join(cmd) + "\n")
        log.write("CWD: " + script_dir + "\n\n")
        log.flush()
        proc = subprocess.run(
            cmd,
            cwd=script_dir,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=args.timeout,
            text=True,
        )
    elapsed = time.perf_counter() - start
    return proc.returncode, elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Run DSE distance-card sanity tests for selected pairwise instances."
    )
    parser.add_argument(
        "datasets",
        nargs="*",
        help="Datasets or aliases, e.g. g3 g4 g11 g12 g13",
    )
    parser.add_argument("--solve-mode", default="assumptions", choices=["first", "assumptions", "incremental"])
    parser.add_argument(
        "--type-card",
        type=int,
        nargs="+",
        default=[1, 2, 3, 4, 5, 6, 7, 8],
        help="Exactly-one cardinality encoding(s).",
    )
    parser.add_argument("--distance-mode", default="card", choices=["pairwise", "card"])
    parser.add_argument(
        "--distance-card",
        type=int,
        nargs="+",
        default=[1, 2, 3, 4, 5, 6, 7, 8],
        help="Distance AMO cardinality encoding(s).",
    )
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per run in seconds.")
    parser.add_argument(
        "--scripts",
        nargs="+",
        default=["pairwise.py"],
        choices=["pairwise.py", "pairwise_no_preprocessing.py"],
        help="Which encoders to run.",
    )
    parser.add_argument("--log-dir", default=os.path.join("results", "distance_card_tests"))
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    datasets = [normalize_dataset(x) for x in (args.datasets or DEFAULT_DATASETS)]
    run_id = time.strftime("run_%Y%m%d_%H%M%S") + f"_{os.getpid()}"
    log_root = os.path.join(script_dir, args.log_dir, run_id)
    os.makedirs(log_root, exist_ok=True)

    print("Datasets:", ", ".join(datasets))
    print("Scripts:", ", ".join(args.scripts))
    print("solve_mode:", args.solve_mode)
    print("type_card:", ", ".join(format_encoding(x) for x in args.type_card))
    print("distance_mode:", args.distance_mode)
    print("distance_card:", ", ".join(format_encoding(x) for x in args.distance_card))
    print("timeout:", args.timeout)
    print("log_dir:", log_root)
    print()

    failures = 0
    for type_card in args.type_card:
        for distance_card in args.distance_card:
            config = f"eo{type_card}_dist{distance_card}"
            for script_name in args.scripts:
                group = "processing" if script_name == "pairwise.py" else "no_processing"
                group_dir = os.path.join(log_root, config, group)
                os.makedirs(group_dir, exist_ok=True)

                for dataset in datasets:
                    log_path = os.path.join(group_dir, f"{dataset}.log")
                    print(f"[RUN] {config} {group} {dataset} -> {log_path}")
                    try:
                        returncode, elapsed = run_case(script_dir, script_name, dataset, args, type_card, distance_card, log_path)
                    except subprocess.TimeoutExpired:
                        failures += 1
                        with open(log_path, "a", encoding="utf-8", errors="replace") as log:
                            log.write(f"\n[TIMEOUT] exceeded {args.timeout} seconds\n")
                        print(f"[TIMEOUT] {config} {group} {dataset} after {args.timeout}s")
                        continue

                    if returncode != 0:
                        failures += 1
                        print(f"[FAIL] {config} {group} {dataset}: returncode={returncode}, time={elapsed:.2f}s")
                    else:
                        print(f"[OK] {config} {group} {dataset}: time={elapsed:.2f}s")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

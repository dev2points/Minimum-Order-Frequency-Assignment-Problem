import argparse
import csv
import os
import re
import subprocess
import sys
import time


DEFAULT_DATASETS = [
    "graph04",
]

ALIASES = {
    "g1": "graph01",
    "g01": "graph01",
    "g2": "graph02",
    "g02": "graph02",
    "g3": "graph03",
    "g03": "graph03",
    "g4": "graph04",
    "g04": "graph04",
    "g5": "graph05",
    "g05": "graph05",
    "g6": "graph06",
    "g06": "graph06",
    "g7": "graph07",
    "g07": "graph07",
    "g8": "graph08",
    "g08": "graph08",
    "g9": "graph09",
    "g09": "graph09",
    "g10": "graph10",
    "g11": "graph11",
    "g12": "graph12",
    "g13": "graph13",
    "g14": "graph14",
    "s1": "scen01",
    "s01": "scen01",
    "s2": "scen02",
    "s02": "scen02",
    "s3": "scen03",
    "s03": "scen03",
    "s4": "scen04",
    "s04": "scen04",
    "s5": "scen05",
    "s05": "scen05",
    "s6": "scen06",
    "s06": "scen06",
    "s7": "scen07",
    "s07": "scen07",
    "s8": "scen08",
    "s08": "scen08",
    "s9": "scen09",
    "s09": "scen09",
    "s10": "scen10",
    "s11": "scen11",
    "t200.1": "TUD200.1",
    "t200.2": "TUD200.2",
    "t200.3": "TUD200.3",
    "t200.4": "TUD200.4",
    "t200.5": "TUD200.5",
    "t916.1": "TUD916.1",
    "t916.2": "TUD916.2",
    "t916.3": "TUD916.3",
    "t916.4": "TUD916.4",
    "t916.5": "TUD916.5",
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


def last_regex_value(text, pattern, cast):
    matches = re.findall(pattern, text)
    if not matches:
        return ""
    try:
        return cast(matches[-1])
    except ValueError:
        return ""


def parse_log(log_path):
    with open(log_path, "r", encoding="utf-8", errors="replace") as log:
        text = log.read()

    return {
        "assignment_vars": last_regex_value(text, r"Number of assignment variables:\s+(\d+)", int),
        "exactly_one_clauses": last_regex_value(text, r"Number of clauses for exactly one constraints:\s+(\d+)", int),
        "distance_clauses": last_regex_value(text, r"Number of clauses for distance constraints:\s+(\d+)", int),
        "label_vars": last_regex_value(text, r"Number of label variables:\s+(\d+)", int),
        "label_clauses": last_regex_value(text, r"Number of clauses for label constraints:\s+(\d+)", int),
        "cardinality_clauses": last_regex_value(text, r"Number of clauses for cardinality constraints:\s+(\d+)", int),
        "final_labels": last_regex_value(text, r"Number of lables used:\s+(\d+)", int),
        "optimal_labels": last_regex_value(text, r"Optimal number of labels used:\s+(\d+)", int),
        "reported_time_sec": last_regex_value(text, r"Total time:\s+([0-9.]+) seconds", float),
        "memory_mb": last_regex_value(text, r"Memory used:\s+([0-9.]+) MB", float),
    }


def write_summary(log_root, rows):
    fields = [
        "dataset",
        "group",
        "script",
        "solve_mode",
        "type_card",
        "type_card_name",
        "distance_mode",
        "distance_card",
        "distance_card_name",
        "status",
        "returncode",
        "wall_time_sec",
        "reported_time_sec",
        "memory_mb",
        "optimal_labels",
        "final_labels",
        "assignment_vars",
        "exactly_one_clauses",
        "distance_clauses",
        "label_vars",
        "label_clauses",
        "cardinality_clauses",
        "log_path",
    ]

    csv_path = os.path.join(log_root, "summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    md_path = os.path.join(log_root, "summary.md")
    md_fields = [
        "dataset",
        "group",
        "type_card",
        "distance_card",
        "status",
        "wall_time_sec",
        "reported_time_sec",
        "memory_mb",
        "optimal_labels",
        "final_labels",
        "distance_clauses",
        "cardinality_clauses",
    ]
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write("| " + " | ".join(md_fields) + " |\n")
        md_file.write("| " + " | ".join(["---"] * len(md_fields)) + " |\n")
        for row in rows:
            md_file.write("| " + " | ".join(str(row.get(field, "")) for field in md_fields) + " |\n")


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
    rows = []
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
                        row = {
                            "dataset": dataset,
                            "group": group,
                            "script": script_name,
                            "solve_mode": args.solve_mode,
                            "type_card": type_card,
                            "type_card_name": ENCODING_NAMES.get(type_card, "unknown"),
                            "distance_mode": args.distance_mode,
                            "distance_card": distance_card,
                            "distance_card_name": ENCODING_NAMES.get(distance_card, "unknown"),
                            "status": "TIMEOUT",
                            "returncode": "",
                            "wall_time_sec": args.timeout,
                            "log_path": log_path,
                        }
                        row.update(parse_log(log_path))
                        rows.append(row)
                        write_summary(log_root, rows)
                        print(f"[TIMEOUT] {config} {group} {dataset} after {args.timeout}s")
                        continue

                    status = "OK" if returncode == 0 else "FAIL"
                    row = {
                        "dataset": dataset,
                        "group": group,
                        "script": script_name,
                        "solve_mode": args.solve_mode,
                        "type_card": type_card,
                        "type_card_name": ENCODING_NAMES.get(type_card, "unknown"),
                        "distance_mode": args.distance_mode,
                        "distance_card": distance_card,
                        "distance_card_name": ENCODING_NAMES.get(distance_card, "unknown"),
                        "status": status,
                        "returncode": returncode,
                        "wall_time_sec": f"{elapsed:.2f}",
                        "log_path": log_path,
                    }
                    row.update(parse_log(log_path))
                    rows.append(row)
                    write_summary(log_root, rows)

                    if returncode != 0:
                        failures += 1
                        print(f"[FAIL] {config} {group} {dataset}: returncode={returncode}, time={elapsed:.2f}s")
                    else:
                        print(f"[OK] {config} {group} {dataset}: time={elapsed:.2f}s")

    print()
    print("summary_csv:", os.path.join(log_root, "summary.csv"))
    print("summary_md:", os.path.join(log_root, "summary.md"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

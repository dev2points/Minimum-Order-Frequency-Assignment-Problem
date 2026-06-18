from __future__ import annotations

import argparse
import csv
import math
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


METHODS = ["POSE_INCSC", "POSE_INC", "DSE_INCSC", "GUR", "CPX_CP", "CPX_MP"]
LEGACY_WIDE_METHODS = ["POSE_INCSC", "POSE_INC", "DSE_INCSC", "GUR", "CPX_MP", "CPX_CP"]

NS_MAIN = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
NS_REL = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}


def canonical_bench_key(name: str) -> str:
    raw = str(name).strip()
    low = raw.lower()

    match = re.match(r"^scen(\d+)$", low)
    if match:
        return f"C{int(match.group(1)):02d}"

    match = re.match(r"^graph(\d+)$", low)
    if match:
        return f"G{int(match.group(1)):02d}"

    match = re.match(r"^([cg])(\d+)$", raw, flags=re.IGNORECASE)
    if match:
        return f"{match.group(1).upper()}{int(match.group(2)):02d}"

    return raw


def normalize_status(value: str) -> str:
    raw = str(value).strip().upper()
    if raw in {"TO", "TIMEOUT", "TL"}:
        return "TO"
    if raw in {"MO", "OOM"}:
        return "MO"
    if raw in {"INF", "INFEASIBLE", "UNSAT", "INFISEABLE", "ÌNF"}:
        return "INF"
    if raw in {"OPT", "OPTIMAL"}:
        return "OPT"
    if raw in {"", "-", "NAN"}:
        return "-"
    return raw


def normalize_solution(value: str) -> str:
    raw = str(value).strip()
    if raw in {"", "-", "nan", "None"}:
        return "-"
    try:
        return str(int(float(raw)))
    except ValueError:
        return raw


def normalize_metric_value(metric: str, value: str | float | int | None) -> str:
    if metric == "Status":
        return normalize_status("" if value is None else str(value))
    if metric == "Solution":
        return normalize_solution("" if value is None else str(value))
    if value is None or str(value).strip() in {"", "-", "nan", "None"}:
        return "-"
    try:
        return f"{float(value):.2f}"
    except ValueError:
        return str(value).strip()


def floats_match(left: str, right: str, tol: float = 0.011) -> bool:
    try:
        return math.isclose(float(left), float(right), abs_tol=tol)
    except ValueError:
        return left == right


def values_match(metric: str, extracted: str, expected: str) -> bool:
    if metric == "Total time":
        return floats_match(extracted, expected)
    return extracted == expected


def load_extracted_legacy_map(
    extracted_csv: Path,
    source_family: str,
) -> dict[tuple[str, str, str, str, str], str]:
    result: dict[tuple[str, str, str, str, str], str] = {}
    with extracted_csv.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row.get("source_family") != source_family:
                continue
            preprocessing = row["preprocessing"]
            dataset_raw = row["dataset"]
            dataset_final = canonical_bench_key(dataset_raw)
            method = row["method"]

            result[(preprocessing, "raw", dataset_raw, method, "Solution")] = normalize_metric_value(
                "Solution", row.get("report_value")
            )
            result[(preprocessing, "raw", dataset_raw, method, "Total time")] = normalize_metric_value(
                "Total time", row.get("report_time_s")
            )
            result[(preprocessing, "raw", dataset_raw, method, "Status")] = normalize_metric_value(
                "Status", row.get("status")
            )

            result[(preprocessing, "final", dataset_final, method, "Solution")] = normalize_metric_value(
                "Solution", row.get("report_value")
            )
            result[(preprocessing, "final", dataset_final, method, "Total time")] = normalize_metric_value(
                "Total time", row.get("report_time_s")
            )
            result[(preprocessing, "final", dataset_final, method, "Status")] = normalize_metric_value(
                "Status", row.get("status")
            )
    return result


def parse_legacy_wide_csv(csv_path: Path, preprocessing: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = list(csv.reader(csv_file))

    for row in reader[2:]:
        if not row or not row[0].strip():
            continue
        dataset = row[0].strip()
        for index, method in enumerate(LEGACY_WIDE_METHODS):
            base = 1 + index * 3
            rows.append(
                {
                    "preprocessing": preprocessing,
                    "dataset_key_type": "raw",
                    "dataset": dataset,
                    "method": method,
                    "metric": "Solution",
                    "expected": normalize_metric_value("Solution", row[base] if base < len(row) else "-"),
                    "source": str(csv_path),
                }
            )
            rows.append(
                {
                    "preprocessing": preprocessing,
                    "dataset_key_type": "raw",
                    "dataset": dataset,
                    "method": method,
                    "metric": "Total time",
                    "expected": normalize_metric_value("Total time", row[base + 1] if base + 1 < len(row) else "-"),
                    "source": str(csv_path),
                }
            )
            rows.append(
                {
                    "preprocessing": preprocessing,
                    "dataset_key_type": "raw",
                    "dataset": dataset,
                    "method": method,
                    "metric": "Status",
                    "expected": normalize_metric_value("Status", row[base + 2] if base + 2 < len(row) else "-"),
                    "source": str(csv_path),
                }
            )
    return rows


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    shared_strings: list[str] = []
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return shared_strings

    for si in root.findall("main:si", NS_MAIN):
        texts = [node.text or "" for node in si.findall(".//main:t", NS_MAIN)]
        shared_strings.append("".join(texts))
    return shared_strings


def sheet_name_to_target(zf: zipfile.ZipFile) -> dict[str, str]:
    workbook_root = ET.fromstring(zf.read("xl/workbook.xml"))
    rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: f"xl/{rel.attrib['Target']}"
        for rel in rels_root.findall("rel:Relationship", NS_REL)
    }
    return {
        sheet.attrib["name"]: rel_map[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        for sheet in workbook_root.findall("main:sheets/main:sheet", NS_MAIN)
    }


def load_sheet_rows(zf: zipfile.ZipFile, sheet_target: str, shared_strings: list[str]) -> list[dict[str, str]]:
    root = ET.fromstring(zf.read(sheet_target))
    rows: list[dict[str, str]] = []
    for row in root.findall("main:sheetData/main:row", NS_MAIN):
        row_values: dict[str, str] = {}
        for cell in row.findall("main:c", NS_MAIN):
            ref = cell.attrib["r"]
            col = re.match(r"[A-Z]+", ref).group(0)
            value_node = cell.find("main:v", NS_MAIN)
            cell_type = cell.attrib.get("t")
            value = ""
            if cell_type == "s" and value_node is not None:
                value = shared_strings[int(value_node.text)]
            elif cell_type == "inlineStr":
                value = "".join(node.text or "" for node in cell.findall(".//main:t", NS_MAIN))
            elif value_node is not None:
                value = value_node.text or ""
            row_values[col] = value
        rows.append(row_values)
    return rows


def parse_final_results_sheet(workbook_path: Path, sheet_name: str) -> list[dict[str, str]]:
    rows_out: list[dict[str, str]] = []
    with zipfile.ZipFile(workbook_path) as zf:
        shared_strings = load_shared_strings(zf)
        targets = sheet_name_to_target(zf)
        sheet_rows = load_sheet_rows(zf, targets[sheet_name], shared_strings)

    left_columns = ["D", "E", "F", "G", "H", "I"]
    right_columns = ["N", "O", "P", "Q", "R", "S"]

    for row in sheet_rows:
        left_bench = row.get("B", "").strip()
        left_metric = row.get("C", "").strip()
        if left_bench and left_metric in {"Solution", "Total time", "Status"}:
            for col, method in zip(left_columns, METHODS):
                rows_out.append(
                    {
                        "preprocessing": "on",
                        "dataset_key_type": "final",
                        "dataset": left_bench,
                        "method": method,
                        "metric": left_metric,
                        "expected": normalize_metric_value(left_metric, row.get(col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )

        right_bench = row.get("L", "").strip()
        right_metric = row.get("M", "").strip()
        if right_bench and right_metric in {"Solution", "Total time", "Status"}:
            for col, method in zip(right_columns, METHODS):
                rows_out.append(
                    {
                        "preprocessing": "off",
                        "dataset_key_type": "final",
                        "dataset": right_bench,
                        "method": method,
                        "metric": right_metric,
                        "expected": normalize_metric_value(right_metric, row.get(col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )

    return rows_out


def parse_final263_sheet(workbook_path: Path, sheet_name: str) -> list[dict[str, str]]:
    rows_out: list[dict[str, str]] = []
    with zipfile.ZipFile(workbook_path) as zf:
        shared_strings = load_shared_strings(zf)
        targets = sheet_name_to_target(zf)
        sheet_rows = load_sheet_rows(zf, targets[sheet_name], shared_strings)

    left_groups = [
        ("POSE_INCSC", ("B", "C", "D")),
        ("POSE_INC", ("E", "F", "G")),
        ("DSE_INCSC", ("H", "I", "J")),
    ]
    right_groups = [
        ("GUR", ("M", "N", "O")),
        ("CPX_MP", ("P", "Q", "R")),
        ("CPX_CP", ("S", "T", "U")),
    ]

    preprocessing = "on"
    for row in sheet_rows:
        title_a = row.get("A", "").strip().lower()
        if "không pre" in title_a or "khong pre" in title_a:
            preprocessing = "off"
            continue

        left_problem = row.get("A", "").strip()
        right_problem = row.get("L", "").strip()

        if left_problem == "Problem" or right_problem == "Problem":
            continue

        if left_problem:
            for method, (value_col, time_col, status_col) in left_groups:
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": left_problem,
                        "method": method,
                        "metric": "Solution",
                        "expected": normalize_metric_value("Solution", row.get(value_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": left_problem,
                        "method": method,
                        "metric": "Total time",
                        "expected": normalize_metric_value("Total time", row.get(time_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": left_problem,
                        "method": method,
                        "metric": "Status",
                        "expected": normalize_metric_value("Status", row.get(status_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )

        if right_problem:
            for method, (value_col, time_col, status_col) in right_groups:
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": right_problem,
                        "method": method,
                        "metric": "Solution",
                        "expected": normalize_metric_value("Solution", row.get(value_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": right_problem,
                        "method": method,
                        "metric": "Total time",
                        "expected": normalize_metric_value("Total time", row.get(time_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )
                rows_out.append(
                    {
                        "preprocessing": preprocessing,
                        "dataset_key_type": "raw",
                        "dataset": right_problem,
                        "method": method,
                        "metric": "Status",
                        "expected": normalize_metric_value("Status", row.get(status_col, "")),
                        "source": f"{workbook_path}::{sheet_name}",
                    }
                )

    return rows_out


def parse_workbook_sheet(workbook_path: Path, sheet_name: str) -> list[dict[str, str]]:
    if sheet_name == "final 263":
        return parse_final263_sheet(workbook_path, sheet_name)
    return parse_final_results_sheet(workbook_path, sheet_name)


def compare_expected_rows(
    extracted_map: dict[tuple[str, str, str, str, str], str],
    expected_rows: list[dict[str, str]],
    comparison_name: str,
) -> list[dict[str, str]]:
    comparisons: list[dict[str, str]] = []
    for row in expected_rows:
        key = (
            row["preprocessing"],
            row["dataset_key_type"],
            row["dataset"],
            row["method"],
            row["metric"],
        )
        extracted = extracted_map.get(key, "-")
        expected = row["expected"]
        comparisons.append(
            {
                "comparison": comparison_name,
                "source": row["source"],
                "preprocessing": row["preprocessing"],
                "dataset": row["dataset"],
                "method": row["method"],
                "metric": row["metric"],
                "extracted": extracted,
                "expected": expected,
                "match": "1" if values_match(row["metric"], extracted, expected) else "0",
            }
        )
    return comparisons


def compare_workbook_against_both_sources(
    result_map: dict[tuple[str, str, str, str, str], str],
    result2_map: dict[tuple[str, str, str, str, str], str],
    workbook_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in workbook_rows:
        key = (
            row["preprocessing"],
            row["dataset_key_type"],
            row["dataset"],
            row["method"],
            row["metric"],
        )
        workbook_value = row["expected"]
        result_value = result_map.get(key, "-")
        result2_value = result2_map.get(key, "-")
        match_result = values_match(row["metric"], result_value, workbook_value)
        match_result2 = values_match(row["metric"], result2_value, workbook_value)

        if match_result and match_result2:
            verdict = "both"
        elif match_result:
            verdict = "result"
        elif match_result2:
            verdict = "result2"
        else:
            verdict = "neither"

        rows.append(
            {
                "source": row["source"],
                "preprocessing": row["preprocessing"],
                "dataset": row["dataset"],
                "method": row["method"],
                "metric": row["metric"],
                "workbook": workbook_value,
                "result": result_value,
                "result2": result2_value,
                "match_result": "1" if match_result else "0",
                "match_result2": "1" if match_result2 else "0",
                "verdict": verdict,
            }
        )
    return rows


def rows_to_map(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str, str], str]:
    result: dict[tuple[str, str, str, str, str], str] = {}
    for row in rows:
        result[
            (
                row["preprocessing"],
                row["dataset_key_type"],
                row["dataset"],
                row["method"],
                row["metric"],
            )
        ] = row["expected"]
    return result


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["comparison", "source", "preprocessing", "dataset", "method", "metric", "extracted", "expected", "match"])
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict[str, str]], path: Path) -> None:
    mismatch_count = sum(1 for row in rows if row["match"] != "1")
    by_comparison: dict[str, tuple[int, int]] = {}
    for row in rows:
        total, mismatches = by_comparison.get(row["comparison"], (0, 0))
        total += 1
        if row["match"] != "1":
            mismatches += 1
        by_comparison[row["comparison"]] = (total, mismatches)

    lines = [f"total_rows={len(rows)}", f"total_mismatches={mismatch_count}"]
    for name, (total, mismatches) in sorted(by_comparison.items()):
        lines.append(f"{name}: rows={total}, mismatches={mismatches}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_origin_summary(rows: list[dict[str, str]], path: Path) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        verdict = row["verdict"]
        counts[verdict] = counts.get(verdict, 0) + 1

    lines = [f"total_rows={len(rows)}"]
    for verdict in ["result", "result2", "both", "neither"]:
        lines.append(f"{verdict}={counts.get(verdict, 0)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    tools_dir = Path(__file__).resolve().parent
    stats_dir = tools_dir.parent
    source_root = stats_dir.parent
    parser = argparse.ArgumentParser(
        description="Validate legacy Result2 extractions against legacy CSVs and Compare MO-FAP workbook."
    )
    parser.add_argument(
        "--extracted-csv",
        type=Path,
        default=stats_dir / "python_total_times_all_methods.csv",
        help="CSV generated by extract_python_total_times.py",
    )
    parser.add_argument(
        "--preprocess-csv",
        type=Path,
        default=source_root.parent / "CleanCodeToSubmit" / "Min-Order-Frequency-Assignment-Problem" / "visualize" / "result_file" / "preprocess.csv",
        help="Legacy preprocess.csv path.",
    )
    parser.add_argument(
        "--nopreprocess-csv",
        type=Path,
        default=source_root.parent / "CleanCodeToSubmit" / "Min-Order-Frequency-Assignment-Problem" / "visualize" / "result_file" / "nopreprocess.csv",
        help="Legacy nopreprocess.csv path.",
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path(r"C:\Users\ADMIN\Downloads\Compare MO-FAP.xlsx"),
        help="Workbook to validate.",
    )
    parser.add_argument(
        "--workbook-sheet",
        default="final 263",
        help="Workbook sheet to validate.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=stats_dir / "legacy_validation",
        help="Directory for validation outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result2_map = load_extracted_legacy_map(args.extracted_csv.resolve(), "legacy_result2")
    result_map = load_extracted_legacy_map(args.extracted_csv.resolve(), "legacy_result")

    expected_rows: list[dict[str, str]] = []
    expected_rows.extend(parse_legacy_wide_csv(args.preprocess_csv.resolve(), "on"))
    expected_rows.extend(parse_legacy_wide_csv(args.nopreprocess_csv.resolve(), "off"))
    csv_comparisons = compare_expected_rows(result2_map, expected_rows, "legacy_csv")

    workbook_rows = parse_workbook_sheet(args.workbook.resolve(), args.workbook_sheet)
    workbook_map = rows_to_map(workbook_rows)
    workbook_vs_legacy_csv = compare_expected_rows(workbook_map, expected_rows, "workbook_vs_legacy_csv")
    workbook_vs_result = compare_expected_rows(result_map, workbook_rows, "workbook_vs_result")
    workbook_vs_result2 = compare_expected_rows(result2_map, workbook_rows, "workbook_vs_result2")
    workbook_origin = compare_workbook_against_both_sources(result_map, result2_map, workbook_rows)

    all_rows = csv_comparisons + workbook_vs_legacy_csv + workbook_vs_result + workbook_vs_result2
    output_dir = args.output_dir.resolve()
    write_csv(csv_comparisons, output_dir / "legacy_vs_csv.csv")
    write_csv(workbook_vs_legacy_csv, output_dir / "workbook_vs_legacy_csv.csv")
    write_csv(workbook_vs_result, output_dir / "workbook_vs_result.csv")
    write_csv(workbook_vs_result2, output_dir / "workbook_vs_result2.csv")
    write_csv(workbook_origin, output_dir / "workbook_source_comparison.csv")
    write_csv(all_rows, output_dir / "legacy_validation_all.csv")
    write_summary(all_rows, output_dir / "summary.txt")
    write_origin_summary(workbook_origin, output_dir / "workbook_source_summary.txt")

    print(f"Wrote validation outputs to {output_dir}")


if __name__ == "__main__":
    main()

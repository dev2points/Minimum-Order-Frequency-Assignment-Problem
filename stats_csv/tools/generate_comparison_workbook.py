from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


LEGACY_GROUPS = [
    ("PSE nsc_asumptions", "legacy_result2", "POSE_INCSC", "nsc_assumptions"),
    ("PSE tot assumptions", "legacy_result2", "POSE_INC", "tot_assumptions"),
    ("pairwise nsc assumptions", "legacy_result2", "DSE_INCSC", "nsc_assumptions"),
    ("Gurobi", "legacy_result2", "GUR", "gurobi"),
    ("CPLEX/MIP", "legacy_result2", "CPX_MP", "mip"),
    ("CPLEX/CP", "legacy_result2", "CPX_CP", "cp"),
]

NEW_GROUPS = [
    ("Card bitwise", "current", "cardinality", "bitwise"),
    ("Card cardnetwrk", "current", "cardinality", "cardnetwrk"),
    ("Card kmtotalizer", "current", "cardinality", "kmtotalizer"),
    ("Card seqcounter", "current", "cardinality", "seqcounter"),
    ("Card totalizer", "current", "cardinality", "totalizer"),
    ("CP-SAT", "current", "cpsat", "mip_style"),
    ("CP-SAT-CP", "current", "cpsat_cp", "cp_style"),
    ("MaxSAT RC2 POSE", "current", "maxsat_rc2", "pose"),
    ("MaxSAT RC2 DSE km", "current", "maxsat_rc2", "dse_kmtotalizer"),
    ("MaxSAT RC2 DSE ladder", "current", "maxsat_rc2", "dse_ladder"),
    ("MaxSAT RC2 DSE seq", "current", "maxsat_rc2", "dse_seqcounter"),
    ("MaxSAT RC2 DSE tot", "current", "maxsat_rc2", "dse_totalizer"),
    ("evalmaxsat POSE", "current", "evalmaxsat", "pose"),
    ("evalmaxsat DSE 1", "current", "evalmaxsat", "dse_1"),
    ("evalmaxsat DSE 5", "current", "evalmaxsat", "dse_5"),
    ("evalmaxsat DSE 6", "current", "evalmaxsat", "dse_6"),
    ("evalmaxsat DSE 8", "current", "evalmaxsat", "dse_8"),
]


@dataclass(frozen=True)
class ColumnSpec:
    label: str
    source_family: str
    method: str
    variant: str


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

    digits = ""
    for char in lowered:
        if char.isdigit():
            digits += char
        elif digits:
            break
    number = int(digits) if digits else 10**9
    return group, number, lowered


def normalize_status(raw: str) -> str:
    value = str(raw).strip().upper()
    mapping = {
        "OPTIMAL": "OPT",
        "OPT": "OPT",
        "TIMEOUT": "TO",
        "TO": "TO",
        "OUT_OF_MEMORY": "MO",
        "MO": "MO",
        "INFEASIBLE": "INF",
        "INF": "INF",
        "UNKNOWN": "-",
        "": "-",
        "-": "-",
    }
    return mapping.get(value, value)


def format_float(raw: str) -> str:
    text = str(raw).strip()
    if text in {"", "-", "None"}:
        return "-"
    value = float(text)
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def format_solution(raw: str) -> str:
    text = str(raw).strip()
    if text in {"", "-", "None"}:
        return "-"
    return str(int(float(text)))


def load_rows(input_csv: Path) -> list[dict[str, str]]:
    with input_csv.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def build_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str], dict[str, str]]:
    lookup: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row["source_family"],
            row["preprocessing"],
            row["method"],
            row["variant"],
            row["dataset"],
        )
        lookup[key] = row
    return lookup


def collect_datasets(rows: list[dict[str, str]], preprocessing: str) -> list[str]:
    datasets = {
        row["dataset"]
        for row in rows
        if row["preprocessing"] == preprocessing
    }
    return sorted(datasets, key=dataset_sort_key)


def filter_rows_for_columns(
    rows: list[dict[str, str]],
    column_specs: list[ColumnSpec],
) -> list[dict[str, str]]:
    allowed = {
        (spec.source_family, spec.method, spec.variant)
        for spec in column_specs
    }
    return [
        row
        for row in rows
        if (
            row["source_family"],
            row["method"],
            row["variant"],
        ) in allowed
    ]


def build_matrix(
    rows: list[dict[str, str]],
    preprocessing: str,
    column_specs: list[ColumnSpec],
) -> list[list[str]]:
    filtered_rows = filter_rows_for_columns(rows, column_specs)
    lookup = build_lookup(filtered_rows)
    datasets = collect_datasets(filtered_rows, preprocessing)

    matrix: list[list[str]] = []
    header_top = [""]
    for spec in column_specs:
        header_top.extend([spec.label, "", ""])
    matrix.append(header_top)

    header_second = ["Problem"]
    for _ in column_specs:
        header_second.extend(["Value", "Time", "Status"])
    matrix.append(header_second)

    for dataset in datasets:
        row_out = [dataset]
        for spec in column_specs:
            key = (spec.source_family, preprocessing, spec.method, spec.variant, dataset)
            source_row = lookup.get(key)
            if source_row is None:
                row_out.extend(["-", "-", "-"])
                continue
            row_out.extend(
                [
                    format_solution(source_row.get("report_value", "-")),
                    format_float(source_row.get("report_time_s", "-")),
                    normalize_status(source_row.get("status", "-")),
                ]
            )
        matrix.append(row_out)

    total_row = ["Total time"]
    for spec in column_specs:
        total_time = 0.0
        has_time = False
        for dataset in datasets:
            key = (spec.source_family, preprocessing, spec.method, spec.variant, dataset)
            source_row = lookup.get(key)
            if source_row is None:
                continue
            raw_time = source_row.get("report_time_s", "").strip()
            if raw_time in {"", "-", "None"}:
                continue
            total_time += float(raw_time)
            has_time = True
        total_row.extend(["-", format_float(total_time) if has_time else "-", "-"])
    matrix.append(total_row)

    return matrix


def write_csv_table(path: Path, matrix: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(matrix)


def write_xlsx(path: Path, preprocess_matrix: list[list[str]], nopreprocess_matrix: list[list[str]]) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError as exc:
        raise RuntimeError("openpyxl is required to generate the workbook.") from exc

    workbook = Workbook()
    first_sheet = workbook.active
    first_sheet.title = "preprocess"
    sheets = [
        (first_sheet, preprocess_matrix),
        (workbook.create_sheet("nopreprocess"), nopreprocess_matrix),
    ]

    header_fill = PatternFill(fill_type="solid", fgColor="D9EAF7")
    top_fill = PatternFill(fill_type="solid", fgColor="BFD7EE")
    bold_font = Font(bold=True)

    for sheet, matrix in sheets:
        for row_idx, row_values in enumerate(matrix, start=1):
            for col_idx, value in enumerate(row_values, start=1):
                cell = sheet.cell(row=row_idx, column=col_idx, value=value)
                if row_idx == 1:
                    cell.font = bold_font
                    cell.fill = top_fill
                    cell.alignment = Alignment(horizontal="center")
                elif row_idx == 2:
                    cell.font = bold_font
                    cell.fill = header_fill
                    cell.alignment = Alignment(horizontal="center")
                elif col_idx == 1:
                    cell.font = bold_font

        sheet.freeze_panes = "B3"

        for column_cells in sheet.columns:
            values = ["" if cell.value is None else str(cell.value) for cell in column_cells]
            width = min(max(len(value) for value in values) + 2, 24)
            sheet.column_dimensions[column_cells[0].column_letter].width = width

    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)


def default_input_csv(root: Path) -> Path:
    preferred = root / "python_total_times_all_methods.csv"
    if preferred.exists():
        return preferred
    fallback = root / "python_total_times_all_methods_test.csv"
    return fallback


def parse_args() -> argparse.Namespace:
    tools_dir = Path(__file__).resolve().parent
    stats_dir = tools_dir.parent
    parser = argparse.ArgumentParser(description="Generate comparison CSVs and workbook from extracted timing data.")
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=default_input_csv(stats_dir),
        help="Consolidated extracted CSV.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=stats_dir / "generated_comparison",
        help="Output directory for generated CSV/XLSX files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input_csv.resolve())

    columns = [ColumnSpec(*spec) for spec in LEGACY_GROUPS + NEW_GROUPS]
    preprocess_matrix = build_matrix(rows, "on", columns)
    nopreprocess_matrix = build_matrix(rows, "off", columns)

    output_dir = args.output_dir.resolve()
    preprocess_csv = output_dir / "preprocess_new.csv"
    nopreprocess_csv = output_dir / "nopreprocess_new.csv"
    workbook_path = output_dir / "Compare_MO_FAP_new.xlsx"

    write_csv_table(preprocess_csv, preprocess_matrix)
    write_csv_table(nopreprocess_csv, nopreprocess_matrix)
    print(f"Wrote {preprocess_csv}")
    print(f"Wrote {nopreprocess_csv}")
    try:
        write_xlsx(workbook_path, preprocess_matrix, nopreprocess_matrix)
    except RuntimeError as exc:
        print(f"Skipped workbook generation: {exc}")
    else:
        print(f"Wrote {workbook_path}")


if __name__ == "__main__":
    main()

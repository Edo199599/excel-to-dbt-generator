from pipeline_generator.parsers.excel_inspector import (
    inspect_sheet,
    inspect_workbook,
)

from pipeline_generator.reports.inspection_report import (
    build_inspection_report,
    save_text_report,
)

import shutil
from pathlib import Path
import argparse

OUTPUT_DIR = "generated"


def reset_generated_dir(output_dir: str) -> None:
    """
    Remove and recreate the generated output directory.

    This avoids keeping stale files from previous runs.
    """
    path = Path(output_dir)

    if path.name != "generated":
        raise ValueError(
            f"Refusing to delete non-generated directory: {path}"
        )

    if path.exists():
        shutil.rmtree(path)

    path.mkdir(parents=True, exist_ok=True)


def print_inspection(inspection: dict) -> None:
    """
    Print a readable inspection summary for one sheet.
    """
    print(f"\n--- {inspection['sheet_name']} ---")
    print(f"Rows: {inspection['rows']}")
    print(f"Columns: {inspection['columns']}")
    print(f"Detected header row: {inspection['header_row']}")
    print(f"Candidate sheet: {inspection['is_candidate']}")

    print("Metadata:")
    for key, value in inspection["metadata"].items():
        print(f"- {key}: {value}")

    if not inspection["is_candidate"]:
        return

    print(f"Rows after cleaning: {inspection['rows_after_cleaning']}")

    column_inspection = inspection["column_inspection"]

    print("Missing standard columns:")
    for column in column_inspection["missing_columns"]:
        print(f"- {column}")

    print("Present aliases:")
    for alias_name, matched_columns in column_inspection["present_aliases"].items():
        print(f"- {alias_name}: {matched_columns}")

    print("Ignored columns:")
    for column in column_inspection["ignored_columns"]:
        print(f"- {column}")

    print("Unknown columns:")
    for column in column_inspection["unknown_columns"]:
        print(f"- {column}")

    print("Warnings:")
    for warning in inspection["warnings"]:
        print(f"- [{warning['severity']}] {warning['code']}: {warning['message']}")


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the inspection command.
    """
    parser = argparse.ArgumentParser(
        description="Inspect Excel technical specifications."
    )
    parser.add_argument(
        "--excel",
        required=True,
        help="Path to the Excel specification file.",
    )
    parser.add_argument(
        "--sheet",
        required=False,
        default=None,
        help="Optional sheet name to inspect. If omitted, all sheets are inspected.",
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    excel_path = args.excel
    selected_sheet_name = args.sheet
    output_dir = OUTPUT_DIR

    reset_generated_dir(output_dir)

    if selected_sheet_name:
        inspections = [
            inspect_sheet(
                excel_path=excel_path,
                sheet_name=selected_sheet_name,
            )
        ]
    else:
        inspections = inspect_workbook(excel_path)

    for inspection in inspections:
        print_inspection(inspection)
    
    for inspection in inspections:
        sheet_name = inspection["sheet_name"]

        report_text = build_inspection_report([inspection])

        save_text_report(
            report_text=report_text,
            output_path=f"{output_dir}/{sheet_name}/inspection_report.md",
        )

        print(
            f"\nInspection report saved to "
            f"{output_dir}/{sheet_name}/inspection_report.md"
        )
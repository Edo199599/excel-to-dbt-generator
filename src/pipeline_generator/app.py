from parsers.excel_inspector import (
    inspect_sheet,
    inspect_workbook,
)

from reports.inspection_report import (
    build_inspection_report,
    save_text_report,
)

import shitil
from pathlib import Path



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


if __name__ == "__main__":
    excel_path = "input/tracciato_prova_SC.xlsx"

    # Set this to a sheet name to inspect only one sheet.
    # Set it to None to inspect the whole workbook.
    selected_sheet_name = None
    # selected_sheet_name = None

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

    report_text = build_inspection_report(inspections)

    save_text_report(
        report_text=report_text,
        output_path="generated/inspection_report.md",
    )

    print("\nInspection report saved to generated/inspection_report.md")
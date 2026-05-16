from pathlib import Path
import pandas as pd


def list_sheet_names(excel_path: str) -> list[str]:
    """
    Read an Excel file and return the list of sheet names.
    """
    path = Path(excel_path)

    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    excel_file = pd.ExcelFile(path)
    return excel_file.sheet_names


if __name__ == "__main__":
    excel_path = "input/tracciato_prova.xlsx"

    sheet_names = list_sheet_names(excel_path)

    print("Sheets found:")
    for sheet_name in sheet_names:
        print(f"- {sheet_name}")
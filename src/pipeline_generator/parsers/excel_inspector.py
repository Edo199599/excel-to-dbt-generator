from pathlib import Path
import pandas as pd

EXPECTED_HEADER_KEYWORDS = {
    "NOME CAMPO",
    "ESPRESSIONE",
    "FORMATO",
    "LUNGHEZZA",
    "IMPORTARE",
}

EXPECTED_MAPPING_COLUMNS = {
    "ID",
    "SCD",
    "PK",
    "NOME CAMPO",
    "ESPRESSIONE",
    "FORMATO",
    "LUNGHEZZA",
    "CAMPO PII",
    "IMPORTARE",
    "FLUSSO BRONZE LAYER",
    "COD CAMPO BRONZE LAYER",
    "DESCRIZIONE CAMPO BRONZE LAYER",
    "NOME CAMPO BRONZE LAYER",
    "DESCRIZIONE FUNZIONALE",
    "FORMATO.1",
    "PK.1",
}

ALIAS_COLUMNS = {
    "SOURCE_DATATYPE": {"DATATYPE", "DATATYPE SORG"},
}

IGNORED_COLUMNS = {
    "DUBBI",
    "RISPOSTE",
}

def list_sheet_names(excel_path: str) -> list[str]:
    """
    Read an Excel file and return the list of sheet names.
    """
    path = Path(excel_path)

    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    excel_file = pd.ExcelFile(path)
    return excel_file.sheet_names


def inspect_sheet_shape(excel_path: str, sheet_name: str) -> dict:
    """
    Read a single sheet and return basic shape information.
    """

    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)

    return {
        "sheet_name": sheet_name,
        "rows": df.shape[0],
        "columns": df.shape[1],
    }


def preview_sheet(excel_path: str, sheet_name: str, n_rows: int = 8) -> pd.DataFrame:
    """
    Read the first rows of a sheet without assuming where the header is.
    """
    return pd.read_excel(
        excel_path,
        sheet_name=sheet_name,
        header=None,
        nrows=n_rows,
    )


def find_header_row(preview_df: pd.DataFrame) -> int | None:
    """
    Try to identify the header row by searching for expected column names.
    """
    for row_index, row in preview_df.iterrows():
        row_values = {
            str(value).strip().upper()
            for value in row.tolist()
            if pd.notna(value)
        }

        matched_keywords = EXPECTED_HEADER_KEYWORDS.intersection(row_values)

        if len(matched_keywords) >= 3:
            return row_index

    return None

def is_candidate_sheet(header_row: int | None) -> bool:
    """
    Decide if a sheet looks like a technical/mapping sheet.
    """
    return header_row is not None

def read_sheet_with_detected_header(
    excel_path: str,
    sheet_name: str,
    header_row: int,
) -> pd.DataFrame:
    """
    Read a sheet using the detected header row as dataframe columns.
    """
    return pd.read_excel(
        excel_path,
        sheet_name=sheet_name,
        header=header_row,
    )

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove empty/unnamed columns and strip column names.
    """
    cleaned_df = df.copy()

    cleaned_df.columns = [
        str(column).strip()
        for column in cleaned_df.columns
    ]

    columns_to_keep = [
        column
        for column in cleaned_df.columns
        if not column.startswith("Unnamed:")
    ]

    cleaned_df = cleaned_df[columns_to_keep]

    return cleaned_df.dropna(how="all")


def inspect_columns(df: pd.DataFrame) -> dict:
    """
    Compare detected columns with expected, alias, ignored and unknown columns.
    """
    detected_columns = {
        str(column).strip().upper()
        for column in df.columns
    }

    present_columns = sorted(
        EXPECTED_MAPPING_COLUMNS.intersection(detected_columns)
    )

    missing_columns = sorted(
        EXPECTED_MAPPING_COLUMNS.difference(detected_columns)
    )

    present_aliases = {}

    for alias_name, alias_options in ALIAS_COLUMNS.items():
        matched_aliases = sorted(alias_options.intersection(detected_columns))

        if matched_aliases:
            present_aliases[alias_name] = matched_aliases

    all_alias_columns = set().union(*ALIAS_COLUMNS.values())

    ignored_columns = sorted(
        IGNORED_COLUMNS.intersection(detected_columns)
    )

    known_columns = (
        EXPECTED_MAPPING_COLUMNS
        .union(IGNORED_COLUMNS)
        .union(all_alias_columns)
    )

    unknown_columns = sorted(
        detected_columns.difference(known_columns)
    )

    return {
        "present_columns": present_columns,
        "missing_columns": missing_columns,
        "present_aliases": present_aliases,
        "ignored_columns": ignored_columns,
        "unknown_columns": unknown_columns,
    }


def inspect_sheet(excel_path: str, sheet_name: str) -> dict:
    """
    Inspect a single sheet and return structured information.
    """
    shape_info = inspect_sheet_shape(excel_path, sheet_name)
    preview = preview_sheet(excel_path, sheet_name)

    header_row = find_header_row(preview)
    candidate = is_candidate_sheet(header_row)

    inspection = {
        "sheet_name": sheet_name,
        "rows": shape_info["rows"],
        "columns": shape_info["columns"],
        "header_row": header_row,
        "is_candidate": candidate,
        "column_inspection": None,
    }

    if not candidate:
        return inspection

    df = read_sheet_with_detected_header(
        excel_path=excel_path,
        sheet_name=sheet_name,
        header_row=header_row,
    )

    clean_df = clean_columns(df)
    inspection["rows_after_cleaning"] = len(clean_df)
    inspection["column_inspection"] = inspect_columns(clean_df)

    return inspection




if __name__ == "__main__":
    excel_path = "input/tracciato_prova_SC.xlsx"

    sheet_names = list_sheet_names(excel_path)

    for sheet_name in sheet_names:
        inspection = inspect_sheet(excel_path, sheet_name)

        print(f"\n--- {inspection['sheet_name']} ---")
        print(f"Rows: {inspection['rows']}")
        print(f"Columns: {inspection['columns']}")
        print(f"Detected header row: {inspection['header_row']}")
        print(f"Candidate sheet: {inspection['is_candidate']}")

        if inspection["is_candidate"]:
            print(f"Rows after cleaning: {inspection['rows_after_cleaning']}")

            column_inspection = inspection["column_inspection"]

            print("Missing expected columns:")
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
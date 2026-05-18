from pathlib import Path


def build_inspection_report(inspections: list[dict]) -> str:
    """
    Build a markdown report from sheet inspections.
    """
    lines = []

    lines.append("# Excel Inspection Report")
    lines.append("")

    for inspection in inspections:
        lines.append(f"## {inspection['sheet_name']}")
        lines.append("")
        lines.append(f"- Rows: {inspection['rows']}")
        lines.append(f"- Columns: {inspection['columns']}")
        lines.append(f"- Detected header row: {inspection['header_row']}")
        lines.append(f"- Candidate sheet: {inspection['is_candidate']}")
        lines.append("")

        if inspection["metadata"]:
            lines.append("### Metadata")
            lines.append("")

            for key, value in inspection["metadata"].items():
                lines.append(f"- **{key}**: {value}")

            lines.append("")

        if inspection["is_candidate"]:
            column_inspection = inspection["column_inspection"]

            lines.append("### Column inspection")
            lines.append("")

            lines.append("#### Missing standard columns")
            if column_inspection["missing_columns"]:
                for column in column_inspection["missing_columns"]:
                    lines.append(f"- {column}")
            else:
                lines.append("- None")
            lines.append("")

            lines.append("#### Present aliases")
            if column_inspection["present_aliases"]:
                for alias_name, matched_columns in column_inspection["present_aliases"].items():
                    matched_columns_text = ", ".join(matched_columns)
                    lines.append(f"- **{alias_name}**: {matched_columns_text}")
            else:
                lines.append("- None")
            lines.append("")

            lines.append("#### Ignored columns")
            if column_inspection["ignored_columns"]:
                for column in column_inspection["ignored_columns"]:
                    lines.append(f"- {column}")
            else:
                lines.append("- None")
            lines.append("")

            lines.append("#### Unknown columns")
            if column_inspection["unknown_columns"]:
                for column in column_inspection["unknown_columns"]:
                    lines.append(f"- {column}")
            else:
                lines.append("- None")
            lines.append("")

            lines.append("### Warnings")
            lines.append("")

            if inspection["warnings"]:
                for warning in inspection["warnings"]:
                    lines.append(
                        f"- **{warning['severity']}** "
                        f"`{warning['code']}`: {warning['message']}"
                    )
            else:
                lines.append("- None")

            lines.append("")

    return "\n".join(lines)


def save_text_report(report_text: str, output_path: str) -> None:
    """
    Save a text report to disk.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")
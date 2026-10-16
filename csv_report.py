
import csv
import json
import sys
from collections import Counter
from pathlib import Path


def create_report(file_path: str, output_path: str | None = None) -> int:
    path = Path(file_path)

    if not path.is_file():
        print(f"Error: File not found: {path}")
        return 1

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: CSV file has no header.")
                return 1

            columns = reader.fieldnames
            rows = list(reader)

    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Error reading CSV: {error}")
        return 1

    missing = Counter()
    for row in rows:
        for column in columns:
            if row.get(column) is None or not row[column].strip():
                missing[column] += 1

    report = {
        "file": path.name,
        "rows": len(rows),
        "columns": len(columns),
        "column_names": columns,
        "missing_values": dict(missing),
        "duplicate_rows": len(rows) - len(
            {tuple(row.get(c) for c in columns) for row in rows}
        ),
    }

    print(f"File: {report['file']}")
    print(f"Rows: {report['rows']}")
    print(f"Columns: {report['columns']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print("\nColumn analysis:")

    for column in columns:
        values = [
            row.get(column, "").strip()
            for row in rows
            if row.get(column) is not None and row[column].strip()
        ]
        unique_count = len(set(values))
        missing_count = missing[column]
        print(
            f"- {column}: {len(values)} filled, "
            f"{missing_count} missing, {unique_count} unique"
        )

    if output_path:
        output = Path(output_path)
        try:
            output.write_text(
                json.dumps(report, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"\nJSON report saved to: {output}")
        except OSError as error:
            print(f"Error saving report: {error}")
            return 1

    print("\nReport completed successfully.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python csv_report.py <file.csv> [report.json]")
        sys.exit(1)

    sys.exit(create_report(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None))

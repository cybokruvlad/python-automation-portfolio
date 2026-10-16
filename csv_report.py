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

    missing = Counter()
    unique_values: dict[str, set[str]] = {}
    seen_rows: set[tuple[str | None, ...]] = set()
    duplicate_rows = 0
    row_count = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file, strict=True)

            if not reader.fieldnames:
                print("Error: CSV file has no header.")
                return 1

            columns = reader.fieldnames
            if len(columns) != len(set(columns)):
                print("Error: CSV contains duplicate column names.")
                return 1

            unique_values = {column: set() for column in columns}

            for row in reader:
                if None in row:
                    print("Error reading CSV: row has more values than the header.")
                    return 1

                row_count += 1
                row_key = tuple(row.get(column) for column in columns)

                if row_key in seen_rows:
                    duplicate_rows += 1
                else:
                    seen_rows.add(row_key)

                for column in columns:
                    value = row.get(column)
                    if value is None or not value.strip():
                        missing[column] += 1
                    else:
                        unique_values[column].add(value.strip())

    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Error reading CSV: {error}")
        return 1

    column_stats = {
        column: {
            "filled": row_count - missing[column],
            "missing": missing[column],
            "unique": len(unique_values[column]),
        }
        for column in columns
    }

    report = {
        "file": path.name,
        "rows": row_count,
        "columns": len(columns),
        "column_names": columns,
        "missing_values": dict(missing),
        "column_stats": column_stats,
        "duplicate_rows": duplicate_rows,
    }

    print(f"File: {report['file']}")
    print(f"Rows: {report['rows']}")
    print(f"Columns: {report['columns']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print("\nColumn analysis:")

    for column in columns:
        stats = column_stats[column]
        print(
            f"- {column}: {stats['filled']} filled, "
            f"{stats['missing']} missing, {stats['unique']} unique"
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

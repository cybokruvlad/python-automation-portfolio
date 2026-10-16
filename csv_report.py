import csv
import sys
from pathlib import Path


def create_report(file_path: str) -> None:
    path = Path(file_path)

    if not path.is_file():
        print(f"Error: File not found: {path}")
        return

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: CSV file has no header.")
                return

            rows = list(reader)

        print(f"File: {path.name}")
        print(f"Rows: {len(rows)}")
        print(f"Columns: {len(reader.fieldnames)}")
        print("\nColumn names:")

        for column in reader.fieldnames:
            print(f"- {column}")

        print("\nReport completed successfully.")

    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Error reading CSV: {error}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_report.py <file.csv>")
        sys.exit(1)

    create_report(sys.argv[1])

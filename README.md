# Python CSV Report Tool

A lightweight command-line tool for analyzing CSV files and generating data quality reports in the terminal or JSON format.

## Features

- Reads CSV files using UTF-8, including files with a UTF-8 BOM.
- Reports the number of rows and columns.
- Lists column names.
- Counts filled and missing values for each column.
- Counts unique, non-empty values for each column.
- Detects duplicate rows.
- Exports detailed JSON reports with optional per-column statistics.
- Rejects duplicate column names and malformed CSV input.
- Handles missing files, empty files, reading errors, and JSON export errors.
- Processes CSV records incrementally instead of loading all row dictionaries at once.

## Requirements

- Python 3.10 or newer.

## Usage

Analyze a CSV file:

```powershell
python .\csv_report.py .\example.csv
```

Export the report to JSON:

```powershell
python .\csv_report.py .\example.csv .\report.json
```

The JSON report includes the input filename, row and column counts, column names, missing-value counts, per-column statistics, and duplicate-row count.

## Development Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

## Quality Checks

Run the linter:

```powershell
python -m ruff check .
```

Run the test suite:

```powershell
python -m pytest -v
```

GitHub Actions runs Ruff and the test suite on pushes and pull requests.

## Example

The included `example.csv` contains three records and three columns. The expected summary is:

- Rows: 3
- Columns: 3
- Duplicate rows: 0

## Project Status

Portfolio project with automated tests for report generation, missing values, JSON export, invalid inputs, UTF-8 BOM handling, duplicate column headers, and larger CSV files.

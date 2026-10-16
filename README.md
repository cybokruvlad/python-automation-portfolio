
# Python CSV Report Tool

A command-line tool that analyzes CSV files and generates useful data quality statistics.

## Features

- Reads CSV files using UTF-8 encoding.
- Reports the number of rows and columns.
- Lists column names.
- Counts filled and missing values per column.
- Counts unique values per column.
- Detects duplicate rows.
- Optionally exports a JSON report.
- Handles missing files and CSV reading errors.

## Requirements

- Python 3.10 or newer.

## Usage

Analyze a CSV file:

```powershell
python .\csv_report.py .\example.csv
```

Save the analysis as JSON:

```powershell
python .\csv_report.py .\example.csv .\report.json
```

## Example

For the included `example.csv`, the tool reports 3 rows, 3 columns, and 0 duplicate rows.

## Project Status

Personal portfolio project. Tested locally with valid CSV data, missing files, missing values, duplicate rows, and JSON export.
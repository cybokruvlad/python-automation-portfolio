import json

from csv_report import create_report


def test_create_report_counts_rows_columns_and_duplicates(tmp_path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,city\nHoussam,Rabat\nSara,Casablanca\nHoussam,Rabat\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file))

    output = capsys.readouterr().out
    assert result == 0
    assert "Rows: 3" in output
    assert "Columns: 2" in output
    assert "Duplicate rows: 1" in output


def test_create_report_counts_missing_values(tmp_path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,city\nHoussam,Rabat\nSara,\n,Sale\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file))

    output = capsys.readouterr().out
    assert result == 0
    assert "- name: 2 filled, 1 missing, 2 unique" in output
    assert "- city: 2 filled, 1 missing, 2 unique" in output


def test_create_report_exports_json(tmp_path):
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "report.json"
    csv_file.write_text(
        "name,city\nHoussam,Rabat\nSara,Casablanca\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file), str(json_file))

    assert result == 0
    report = json.loads(json_file.read_text(encoding="utf-8"))
    assert report["rows"] == 2
    assert report["columns"] == 2
    assert report["column_names"] == ["name", "city"]
    assert report["duplicate_rows"] == 0


def test_create_report_rejects_missing_file(tmp_path, capsys):
    result = create_report(str(tmp_path / "missing.csv"))

    output = capsys.readouterr().out
    assert result == 1
    assert "Error: File not found:" in output


def test_create_report_rejects_empty_file(tmp_path, capsys):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    result = create_report(str(csv_file))

    output = capsys.readouterr().out
    assert result == 1
    assert "CSV file has no header." in output

def test_create_report_accepts_utf8_bom(tmp_path, capsys):
    csv_file = tmp_path / "bom.csv"
    csv_file.write_text(
        "\ufeffname,city\nHoussam,Rabat\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file))

    output = capsys.readouterr().out
    assert result == 0
    assert "Columns: 2" in output
    assert "name" in output


def test_create_report_handles_duplicate_column_names(tmp_path, capsys):
    csv_file = tmp_path / "duplicate_headers.csv"
    csv_file.write_text(
        "name,name\nHoussam,Chaoui\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file))

    assert result == 1
    assert "duplicate" in capsys.readouterr().out.lower()


def test_create_report_rejects_invalid_csv(tmp_path, capsys):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        'name,age\n"Houssam,20\n',
        encoding="utf-8",
    )

    result = create_report(str(csv_file))

    assert result == 1
    assert "Error reading CSV:" in capsys.readouterr().out


def test_create_report_reports_json_write_error(tmp_path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name\nHoussam\n", encoding="utf-8")
    output_path = tmp_path / "missing_directory" / "report.json"

    result = create_report(str(csv_file), str(output_path))

    assert result == 1
    assert "Error saving report:" in capsys.readouterr().out

def test_json_report_includes_per_column_statistics(tmp_path):
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "report.json"
    csv_file.write_text(
        "name,city\nHoussam,Rabat\nSara,\nHoussam,Rabat\n",
        encoding="utf-8",
    )

    result = create_report(str(csv_file), str(json_file))

    assert result == 0
    report = json.loads(json_file.read_text(encoding="utf-8"))
    assert report["column_stats"]["name"] == {
        "filled": 3,
        "missing": 0,
        "unique": 2,
    }
    assert report["column_stats"]["city"] == {
        "filled": 2,
        "missing": 1,
        "unique": 1,
    }


def test_create_report_handles_large_csv(tmp_path):
    csv_file = tmp_path / "large.csv"
    with csv_file.open("w", encoding="utf-8", newline="") as file:
        file.write("id,value\n")
        for index in range(20_000):
            file.write(f"{index},item-{index % 100}\n")

    result = create_report(str(csv_file))

    assert result == 0

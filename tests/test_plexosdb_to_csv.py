import csv
import pytest
from plexosdb.db import ClassEnum


@pytest.fixture
def db(tmp_path, db_instance_with_schema):
    # This fixture is defined to provide a fresh DB for each test
    yield db_instance_with_schema


def test_to_csv_basic(db, tmp_path):
    db.add_object(ClassEnum.Generator, "Gen1", description="Test generator")
    # Use a valid category for Generator, e.g., 'Generator' itself or another valid category
    db.add_category("Generator", ClassEnum.Generator)
    db.update_object(ClassEnum.Generator, "Gen1", new_name="Gen1", new_category="Generator")
    db.add_property(ClassEnum.Generator, "Gen1", "Max Capacity", 100.0)
    out_dir = tmp_path / "csv_export"
    db.to_csv(out_dir)
    expected_files = [
        "Objects.csv",
        "Categories.csv",
        "Memberships.csv",
        "CustomColumns.csv",
        "Attributes.csv",
        "Properties.csv",
        "Reports.csv",
        "Config.csv",
    ]
    for fname in expected_files:
        fpath = out_dir / fname
        assert fpath.exists(), f"Missing CSV: {fname}"
        with open(fpath, newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            headers = next(reader)
            assert isinstance(headers, list)
            assert len(headers) > 0

    with open(out_dir / "Objects.csv", newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
        assert any(r["name"] == "Gen1" for r in rows)
    with open(out_dir / "Properties.csv", newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
        assert any(r["property"] == "Max Capacity" for r in rows)


def test_to_csv_empty_tables(db, tmp_path):
    out_dir = tmp_path / "csv_empty"
    db.to_csv(out_dir)
    for fname in [
        "Objects.csv",
        "Categories.csv",
        "Memberships.csv",
        "CustomColumns.csv",
        "Attributes.csv",
        "Properties.csv",
        "Reports.csv",
    ]:
        fpath = out_dir / fname
        assert fpath.exists()
        with open(fpath, newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            headers = next(reader)
            assert isinstance(headers, list)
            assert next(reader, None) is None
    # Config.csv may always have a version row, so just check it exists and has at least a header
    fpath = out_dir / "Config.csv"
    assert fpath.exists()
    with open(fpath, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        headers = next(reader)
        assert isinstance(headers, list)

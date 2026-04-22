from __future__ import annotations

import pytest

from plexosdb import ClassEnum, CollectionEnum


def test_delete_scenario_dry_run_reports_without_deleting(db_with_scenarios):
    scenario_name = db_with_scenarios.list_scenarios()[0]

    msgs = db_with_scenarios.delete_scenario(object_name=scenario_name, dry_run=True)

    assert any("Would delete object" in msg for msg in msgs)
    assert db_with_scenarios.check_scenario_exists(scenario_name)


def test_delete_scenario_tag_only_deletes_object_tag(db_with_scenarios):
    data_id = db_with_scenarios.add_property(
        ClassEnum.Generator,
        "thermal-01",
        "Max Capacity",
        110.0,
        scenario="Base",
        band=2,
    )
    scenario_id = db_with_scenarios.get_scenario_id("Base")
    assert db_with_scenarios.check_tag_exists(data_id, scenario_id)

    db_with_scenarios.delete_scenario(object_name="Base", dry_run=False, tag_only=True)

    assert not db_with_scenarios.check_tag_exists(data_id, scenario_id)
    assert db_with_scenarios.check_data_id_exist(data_id)


def test_delete_membership_removes_existing_membership(db_with_topology):
    db_with_topology.delete_membership(
        parent_object_name="thermal-01",
        child_object_name="node-01",
        parent_class=ClassEnum.Generator,
        child_class=ClassEnum.Node,
        collection=CollectionEnum.Nodes,
    )

    with pytest.raises(ValueError, match="Membership not found"):
        db_with_topology.delete_membership(
            parent_object_name="thermal-01",
            child_object_name="node-01",
            parent_class=ClassEnum.Generator,
            child_class=ClassEnum.Node,
            collection=CollectionEnum.Nodes,
        )


def test_delete_membership_requires_resolution_inputs(db_with_topology):
    with pytest.raises(ValueError, match="Either parent_object_id or"):
        db_with_topology.delete_membership(
            child_object_name="node-01",
            child_class=ClassEnum.Node,
            collection=CollectionEnum.Nodes,
        )


def test_delete_attribute_removes_attribute_data_row(db_base):
    db_base.add_object(ClassEnum.Generator, "TestGen")
    db_base.add_attribute(
        ClassEnum.Generator,
        "TestGen",
        attribute_name="Latitude",
        attribute_value=10.1,
    )

    object_id = db_base.get_object_id(ClassEnum.Generator, "TestGen")
    attribute_id = db_base.get_attribute_id(ClassEnum.Generator, "Latitude")
    assert (
        db_base.get_attribute(ClassEnum.Generator, object_name="TestGen", attribute_name="Latitude")[0]
        == 10.1
    )

    db_base.delete_attribute(
        attribute_name="Latitude",
        object_name="TestGen",
        object_class=ClassEnum.Generator,
        object_id=object_id,
        attribute_id=attribute_id,
    )

    assert (
        db_base.query(
            "SELECT 1 FROM t_attribute_data WHERE object_id = ? AND attribute_id = ?",
            (object_id, attribute_id),
        )
        == []
    )


def test_list_classes_and_units_return_rows(db_base):
    classes = db_base.list_classes()
    units = db_base.list_units()

    assert "Generator" in classes
    assert any("MW" in unit.values() for unit in units)


def test_delete_text_with_and_without_class_id(db_with_topology, tmp_path):
    data_file = tmp_path / "profile.csv"
    data_file.write_text("value\n1\n")
    data_id = db_with_topology.add_property(
        ClassEnum.Generator,
        "thermal-01",
        "Rating",
        0.0,
        band=1,
        datafile_text=str(data_file),
    )
    timeslice_class_id = db_with_topology.get_class_id(ClassEnum.Timeslice)
    datafile_class_id = db_with_topology.get_class_id(ClassEnum.DataFile)
    db_with_topology.add_text(ClassEnum.Timeslice, "Peak", data_id)

    db_with_topology.delete_text(data_id, class_id=timeslice_class_id)
    assert (
        db_with_topology.query(
            "SELECT value FROM t_text WHERE data_id = ? AND class_id = ?",
            (data_id, timeslice_class_id),
        )
        == []
    )
    assert db_with_topology.query(
        "SELECT value FROM t_text WHERE data_id = ? AND class_id = ?",
        (data_id, datafile_class_id),
    )

    db_with_topology.delete_text(data_id)
    assert db_with_topology.query("SELECT value FROM t_text WHERE data_id = ?", (data_id,)) == []


def test_upsert_data_text_updates_existing_text_row(db_with_topology, tmp_path):
    data_file = tmp_path / "profile.csv"
    data_file.write_text("value\n1\n")
    data_id = db_with_topology.add_property(
        ClassEnum.Generator,
        "thermal-01",
        "Rating",
        0.0,
        band=1,
        datafile_text=str(data_file),
    )
    class_id = db_with_topology.get_class_id(ClassEnum.DataFile)

    db_with_topology._upsert_data_text(ClassEnum.DataFile, data_id, "updated.csv")

    assert (
        db_with_topology.query(
            "SELECT value FROM t_text WHERE data_id = ? AND class_id = ?",
            (data_id, class_id),
        )[0][0]
        == "updated.csv"
    )


def test_upsert_data_text_inserts_new_text_row(db_with_topology):
    data_id = db_with_topology.add_property(
        ClassEnum.Generator,
        "thermal-01",
        "Fuel Price",
        5.0,
        band=1,
    )
    class_id = db_with_topology.get_class_id(ClassEnum.Timeslice)

    db_with_topology._upsert_data_text(ClassEnum.Timeslice, data_id, "Offpeak")

    assert (
        db_with_topology.query(
            "SELECT value FROM t_text WHERE data_id = ? AND class_id = ?",
            (data_id, class_id),
        )[0][0]
        == "Offpeak"
    )


def test_list_objects_by_class_missing_category_raises(db_with_topology):
    with pytest.raises(Exception, match="does not exist"):
        db_with_topology.list_objects_by_class(ClassEnum.Generator, category="missing-category")

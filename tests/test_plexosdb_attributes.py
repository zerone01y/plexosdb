from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from plexosdb.db import PlexosDB


def test_add_attribute(db_base: PlexosDB):
    from plexosdb.enums import ClassEnum

    db: PlexosDB = db_base
    attribute_id = db.get_attribute_id(ClassEnum.Generator, "Latitude")
    assert attribute_id
    assert attribute_id == 1

    _ = db.add_object(ClassEnum.Generator, "TestGen")
    attribute_id_insert = db.add_attribute(
        ClassEnum.Generator, "TestGen", attribute_name="Latitude", attribute_value=10.1
    )

    assert attribute_id == attribute_id_insert

    result = db.get_attribute(ClassEnum.Generator, object_name="TestGen", attribute_name="Latitude")[0]
    assert result
    assert result == 10.1


def test_list_attributes(db_base: PlexosDB):
    from plexosdb.enums import ClassEnum

    db: PlexosDB = db_base

    result = db.list_attributes(ClassEnum.Generator)
    assert result
    assert len(result) == 2


def test_update_attribute_updates_existing_value(db_base: PlexosDB):
    from plexosdb.enums import ClassEnum

    db = db_base
    _ = db.add_object(ClassEnum.Generator, "TestGen")
    db.add_attribute(ClassEnum.Generator, "TestGen", attribute_name="Latitude", attribute_value=10.1)

    attribute_data_id = db.update_attribute(
        20.2,
        attribute_name="Latitude",
        object_name="TestGen",
        object_class=ClassEnum.Generator,
    )

    assert attribute_data_id == db.get_attribute_id(ClassEnum.Generator, "Latitude")
    assert db.get_attribute(ClassEnum.Generator, object_name="TestGen", attribute_name="Latitude")[0] == 20.2


def test_update_attribute_inserts_when_missing(db_base: PlexosDB):
    from plexosdb.enums import ClassEnum

    db = db_base
    _ = db.add_object(ClassEnum.Generator, "TestGen")

    attribute_data_id = db.update_attribute(
        30.3,
        attribute_name="Latitude",
        object_name="TestGen",
        object_class=ClassEnum.Generator,
    )

    assert isinstance(attribute_data_id, int)
    assert db.get_attribute(ClassEnum.Generator, object_name="TestGen", attribute_name="Latitude")[0] == 30.3


def test_update_attribute_raises_for_missing_object(db_base: PlexosDB):
    from plexosdb.enums import ClassEnum

    with pytest.raises(Exception):
        db_base.update_attribute(
            1.0,
            attribute_name="Latitude",
            object_name="MissingGen",
            object_class=ClassEnum.Generator,
        )

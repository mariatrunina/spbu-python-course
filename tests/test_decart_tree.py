import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.decart_tree import CartesianTree


@pytest.fixture
def tree():
    """Fixture to create a Cartesian tree for tests."""
    return CartesianTree()


def test_insert_and_get(tree):
    tree["key1"] = "value1"
    tree["key2"] = "value2"
    assert tree["key1"] == "value1"
    assert tree["key2"] == "value2"


def test_update_value(tree):
    tree["key1"] = "value1"
    tree["key1"] = "value_updated"
    assert tree["key1"] == "value_updated"


def test_key_not_found(tree):
    with pytest.raises(KeyError):
        tree["non_existing_key"]


def test_delete(tree):
    tree["key1"] = "value1"
    del tree["key1"]
    with pytest.raises(KeyError):
        tree["key1"]


def test_length(tree):
    tree["key1"] = "value1"
    tree["key2"] = "value2"
    assert len(tree) == 2
    del tree["key1"]
    assert len(tree) == 1


def test_iter(tree):
    tree["key1"] = "value1"
    tree["key2"] = "value2"
    tree["key3"] = "value3"
    assert list(iter(tree)) == ["key1", "key2", "key3"]

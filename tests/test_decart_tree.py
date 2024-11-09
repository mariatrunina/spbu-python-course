import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.decart_tree import CartesianTree


@pytest.fixture
def tree():
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


def test_contains(tree):
    tree["key1"] = "value1"
    assert "key1" in tree
    assert "non_existing_key" not in tree


def test_reverse_order_traversal(tree):
    tree["key1"] = "value1"
    tree["key3"] = "value3"
    tree["key2"] = "value2"
    assert list(tree._in_order(tree.root)) == ["key1", "key2", "key3"]


def test_mutable_mapping_methods(tree):
    tree["key1"] = "value1"
    assert len(tree) == 1
    assert tree["key1"] == "value1"
    assert "key1" in tree
    assert "non_existing_key" not in tree
    del tree["key1"]
    assert len(tree) == 0
    assert "key1" not in tree

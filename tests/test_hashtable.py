from src.navigation.hashtable import HashTable
import pytest


class TestHashTable:
    def test_insert_and_get(self):
        ht = HashTable()
        ht.insert("A101", "Room A101")
        assert ht.get("A101") == "Room A101"

    def test_get_missing_key(self):
        ht = HashTable()
        with pytest.raises(KeyError):
            ht.get("nonexistent")

    def test_delete(self):
        ht = HashTable()
        ht.insert("key1", "val1")
        ht.delete("key1")
        assert ht.contains("key1") is False

    def test_contains(self):
        ht = HashTable()
        ht.insert("foo", "bar")
        assert ht.contains("foo") is True
        assert ht.contains("baz") is False

    def test_keys_and_values(self):
        ht = HashTable()
        ht.insert("a", 1)
        ht.insert("b", 2)
        assert set(ht.keys()) == {"a", "b"}
        assert set(ht.values()) == {1, 2}

    def test_len(self):
        ht = HashTable()
        assert len(ht) == 0
        ht.insert("x", 10)
        assert len(ht) == 1

import os
import shutil
import tempfile 
import unittest

from db import WALStore, WALEntry, MemTable, LSMTree

class TestWALEntry(unittest.TestCase):
    """Tests for the WALEntry serialization helper."""

    def test_set_entry_has_correct_fields(self):
        entry = WALEntry("set", "name", "bruh")
        self.assertEqual(entry.operation, "set")
        self.assertEqual(entry.key, "name")
        self.assertEqual(entry.value, "bruh")

    def test_del_entry_serializes(self):
        entry = WALEntry("del", "name", None)
        data = entry.serialize()
        self.assertIn('"operation": "del"', data)
        self.assertIn('"key": "name"', data)
    
class TestMemTable(unittest.TestCase):

    def test_add_and_get(self):
        mt = MemTable()
        mt.add("bruh", "bruhhh")
        self.assertEqual(mt.get("bruh"), "bruhhh")
    
    def test_overwrite_key(self):
        mt = MemTable()
        mt.add("bruh", "bruhhh")
        mt.add("yo", "fr")
        self.assertEqual(mt.get("yo"), "fr")


class TestLSMTree(unittest.TestCase):
    # okay setUp and tearDown are specially recognized by unittest
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db = LSMTree(self.tmpdir)
        
    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.tmpdir)

    def test_set_get(self):
        self.db.set("name", "jeff")
        self.assertEqual(self.db.get("name"), "jeff")
    
    def test_range_query(self):
        self.db.set("item:001", "apple")
        self.db.set("item:002", "banana")
        self.db.set("item:003", "cherry")
        self.db.set("item:004", "dragonfruit")
        results = dict(self.db.range_query("item:001", "item:003"))
        self.assertEqual(results, {
            "item:001": "apple",
            "item:002": "banana",
            "item:003": "cherry",
        })


if __name__ == "__main__":
    unittest.main()
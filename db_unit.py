import os
import shutil
import tempfile 
import unittest
import threading
import time

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

class TestLSMTreeThreadSafety(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db = LSMTree(self.tmpdir)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.tmpdir)

    def test_concurrent_writes(self):
        errors = []

        def writer(thread_id):
            try:
                for i in range(50):
                    self.db.set(f"thread{thread_id}:key{i:03d}", f"val{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target = writer, args = (t,)) for t in range(10)]
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(errors, [], f"Threads raised errors: {errors}")


    def test_concurrent_deletes(self):
        for i in range(50):
            self.db.set(f"item:{i:03d}", f"val{i}")
        
        errors = []

        def deleter():
            try:
                for i in range(0, 50, 2):
                    self.db.delete(f"item:{i:03d}")
            except Exception as e:
                errors.append(e)

        def reader():
            try:
                for i in range(50):
                    self.db.get(f"item:{i:03d}")
            except Exception as e:
                errors.append(e)

        threads = (
            [threading.Thread(target=deleter) for _ in range(3)] +
            [threading.Thread(target=reader)  for _ in range(3)]
        )
        for t in threads: t.start()
        for t in threads: t.join()

        self.assertEqual(errors, [], f"Concurrent delete errors: {errors}")
        # after all threads done, deleted keys must be gone
        for i in range(0, 50, 2):
            self.assertIsNone(self.db.get(f"item:{i:03d}"))

            
if __name__ == "__main__":
    unittest.main()
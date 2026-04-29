import os
import shutil
import tempfile 
import unittest

from db import WALStore, WALEntry, DatabaseError

class TestWALEntry(unittest.TestCase):
    """Tests for the WALEntry serialization helper."""

    def test_set_entry_has_correct_fields(self):
        entry = WALEntry("set", "name", "bruh")
        self.assertEqual(entry.operation, "set")
        self.assertEqual(entry.key, "name")
        self.assertEqual(entry.value, "bruh")




if __name__ == "__main__":
    unittest.main()
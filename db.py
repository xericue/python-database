import os
import shutil
import pickle
from typing import Any, Dict, Optional, Iterator, Tuple

class DatabaseError(Exception):
    pass

class WALEntry:
    def __init__(self, operation: str, key: str, value: Any):
        self.timestamp = datetime.utcnow().isoformat()
        self.operation = operation # set or del type thing
        self.key = key
        self.value = value

    def serialize(self) -> str:
        # convert entry to string for storage
        return json.dumps({
            'timestamp': self.timestamp,
            'operation': self.operation,
            'key': self.key,
            'value': self.value
        }) # json for readability

class WALStore:
    """
    We keep track of two files: the data_file and the wal_file.

    The data_file keeps all of our data periodically, like a backup.
    The wal_file acts as our transaction log. Sort of like how a kitchen works.
    What?

    Recovery:
    - load the last saved state from data_file
    - replay all operations from WAL file
    """

    # create a new database using a file to store data
    # self.data is the in-memory dictionary
    def __init__(self, data_file: str, wal_file: str):
        self.data_file = data_file
        self.wal_file = wal_file
        self.data = Dict[str, Any] = {} # type hinting
        self._recover() # disk loading
    
    def _append_wal(self, entry: WALEntry):
        """Write an entry to the transaction log."""
        # This works in O(n) WHERE n is the length of entry.serialize()
        # in bytes. The flush and other OS calls are O(1).
        try:
            with open(self.wal_file, "a") as transaction_log:
                transaction_log.write(entry.serialize() + "\n")
                transaction_log.flush() # WRITE it to disk
                os.fsync(transaction_log.fileno()) # force disk write
        except IOError as e:
            raise DatabaseError(f"couldnt track this one in the log bruh: {e}")


    # recovery (longggg list of operations)
    def _load(self):
        try:
            # first try loading the last checkpoint on the data_file
            if os.path.exists(self.data_file):
                with open(self.data_file, "rb") as checkpoint:
                    self.data = pickle.load(checkpoint)
                    # with automatically closes the stream for us
            
            # THEN, replay changes from WAL regardless
            if os.path.exists(self.wal_file):
                with open(self.wal_file, "r") as tracked_log:
                    for line in tracked_log:
                        if line.strip():
                            entry = json.loads(line)
                            
                            if entry["operation"] == "set":
                                # set in data[entry["key"]] to the value Yeah!!!
                                self.data[entry["key"]] = entry["value"]
                        
                            elif entry["operation"] == "del":
                                # DELETE IT!!! SAY GOODBYE!!!
                                self.data.pop(entry["key"], None)
        
        except (IOError, json.JSONDecoreError, pickle.PickleError) as e:
            raise DatabaseError(f"couldnt recover your database twin: {e}")
    
    def set(self, key: str, value: Any): # python typing and SET operation
        """Enter a new KV pair with WAL using 'set'."""
        # MAKE SURE TO SAVE TO WAL FIRST
        entry = WALEntry("set", key, value)
        self._append_wal(entry) # handles disk writing
        self.data[key] = value
    
    def delete(self, key: str):
        """Delete a key with WAL using 'del'."""
        entry = WALEntry("del", key, None)
        self._append_wal(entry) # handles disk writing
        self.data.pop(key, None)
        
    def checkpoint(self):
        """Define a checkpoint of the current state."""
        temp_file = f"{self.data_file}.tmp"
        try:
            # write to temporary file first
            with open(temp_file, "wb") as f:
                pickle.dump(self.data, f)
                f.flush()
                os.fsync(f.fileno())

            # atomically replace old file - 
            # directory management library
            shutil.move(temp_file, self.data_file)

            # Clear WAL - just truncate instead of opening in 'w' mode
            if os.path.exists(self.wal_file):
                with open(self.wal_file, "r+") as f:
                    f.truncate(0)
                    f.flush()
                    os.fsync(f.fileno())
        except IOError as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise DatabaseError(f"Checkpoint failed: {e}")

class MemTable:
    """This is the internal data structure that allows us to maintain a sorted order in memory,
    enabling efficient reads and range queries. New items go in here first, then, when it gets
    full, you file them away in SSTables. This is sort of like a loading dock that gets loaded
    and flushed constantly."""

    def __init__(self, max_size: int = 1000):
        # all entries in the memtable
        # again, think of this as a cache that gets flushed at capacity
        self.entries: List[Tuple[str, Any]] = []
        self.max_size = max_size

    def add(self, key: str, value: Any):
        """Add or update a KV pair."""
        # TODO:
        pass
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from a key."""
        # TODO:
        
        return None
     
    def is_full(self) -> bool:
        """Check if length of entries >= max_size."""
        return len(self.entries) >= self.max_size
    
    def range_scan(self, start: str, end: str) -> Iterator[Tuple[str, Any]]:
        """Scan entries within the key range."""
        # TODO:
        pass



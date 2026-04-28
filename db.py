import os
import pickle
from typing import Any, Dict, Optional

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
        try:
            
        except IOError as e:
            raise DatabaseError(f"Failed to write to WAL: {e}")


    # recovery (longggg list of operations)
    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as new_file: # read binary format
                self.data = pickle.load(new_file) # deserialize byte stream (pickled file) into a Python object
    
    def _save(self):
        with open(self.filename, 'rb') as new_file:
            # pickle.dump() opposes load - serialize Python obj. and write to file in binary format
            pickle.dump(self.data, new_file)
    
    def set(self, key: str, value: Any): # python typing and SET operation
        self.data[key] = value
        self._save() # write to disk immediately
    
    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key) # get the actual thing we want

        
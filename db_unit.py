import os
import pickle
from typing import Any, Dict, Optional

class SimpleStore:
    """
    This is the basis of our database. We get, set, and delete. Of course, 
    with Python classes, we must clearly define our magic method 
    constructor __init__ to initialize a database. We then define a _load
    and a _save function to use internally: _load will call os.path.exists 
    to check if data from the disk exists, and _save will save the data to
    disk. Simple!
    """
    # create a new database using a file to store data
    # self.data is the in-memory dictionary
    def __init__(self, filename, str):
        self.filename = filename
        self.data = Dict[str, Any] = {} # type hinting
        self._load() # disk loading
    
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

    

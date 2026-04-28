import os
import pickle
from typing import Tuple, Any, Dict

class SimpleDatabase(self, filename: str):
    """This class exists simply to serve as a baseline for CRUD operations
    and how it evolves throughout the repository. Our goal is to save, 
    essentially, a Python dictionary to a file with create, read, update,
    and delete operations."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self._load() # load data from disk if it exists

    def _load(self):
        """Load data from disk if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.data = pickle.load(f)
        
    def _save(self):
        """Save data to disk."""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f) # dump the keys and values 

    def set():
        """Update the data in the key-value pair of the dictionary."""
        self.data[key] = value
        self._save() # call save to save it to disk

    def get():
        """Return the data."""
        return self.data.get(key) # data is a dictionary here
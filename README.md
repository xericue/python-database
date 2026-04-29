# Write-Heavy Databse in Python

project overview: this is a write-heavy database implemented from scratch in Python. No SQL or SQLite, just the implementation. systems that require large volumes of data with strict latency requirements for writing more than they read (logging and monitoring systems, financial transaction)

- [x] implement sstable
- [x] implement memtable fully
- [ ] implement the actual LSM tree
- [ ] migrate from a sorted list with binary search in the memtable to a skip list (apparently adjacent to leveldb and rocksdb)
- [ ] generate unit tests
- [ ] personally try the database
- [ ] record a video
- [ ] fix readme


data structure concepts used: LSM tree, database storage, hashing. Since a hash map is a very common data structure used in our homeworks and a database is a well-known tool in almost all apps and companies around the world, I wanted to learn about its implementation a bit more.
Binary search is used in the mem table (literally textbook binary search: the index bisects the list and then inserts if the index is equal to the necessary key in the memtable).

project workflow: explain end-to-end workflow
The major concepts here are the write-ahead log (WAL), memory table (MemTable), (SSTable), and the log-structured merge tree (LSM tree). We want persistence, fast access, and accurate sorting. 

### What's Write-Ahead Logging?
This is essentially keeping a journal of what happened and the changes that will happen BEFORE you apply it to the database. You can make them cute little diary entries. This helps ensure data persistence and recovery! This means that each operation (set, del) will need to log these entries in the WAL - this helps us practice modular programming as well as object oriented programming.

### Isn't this whole thing a "Memory Table?"
Not quite. While our database stores key-value pairs, we use Memory Tables (MemTables) to make our database's writes much faster, providing quick access to recently written data (almost like a cache or sorting tray).

Woah, what's this? the `bisect` library and `bisect_left()` - these are high level Python libraries and functions that allow us to insert values into a sorted list without constant re-sorting. Magically, it's O(logn) (because it uses a binary search to find the insertion point). Python is magic.



performance: average running time of project and/or time complexity

challenges:

improvements:

learning:
### Why use Python Tuple typing?
Type hints are essentially what Python lack. 
typing.Tuple lets us specify a specific number of elements expected and the type of each position, allowing our code to be more /strict/. It's not too horrible though - we could use tuple(float, float) if need be.

real-world relevance:

use of ai-tools:


expected I/O: input of commands (GET/SET/DEL), output: persistent storage and returned user data
space and time complexity: O(1) for most operations

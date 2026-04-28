# python-database

project overview: this is a database implemented from scratch in Python. No SQL or SQLite, just the implementation.

data structure concepts used: LSM tree, database storage, hashing. Since a hash map is a very common data structure used in our homeworks and a database is a well-known tool in almost all apps and companies around the world, I wanted to learn about its implementation a bit more.

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

real-world relevance:

use of ai-tools:


expected I/O: input of commands (GET/SET/DEL), output: persistent storage and returned user data
space and time complexity: O(1) for most operations

150 characters this must be !!!

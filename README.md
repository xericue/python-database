# Write-Heavy Databse in Python

project overview: this is a write-heavy database implemented from scratch in Python. No SQL or SQLite, just the implementation. systems that require large volumes of data with strict latency requirements for writing more than they read (logging and monitoring systems, financial transaction). while my initial goals for this project are silly (store "bruh" -> "gurt", "dylan" -> "goat"), i hope to scale this in the future, possibly for high-frequency trading!

- [x] implement sstable
- [x] implement memtable fully
- [ ] implement the actual LSM tree
- [ ] generate unit tests
- [ ] personally try the database
- [ ] record a video
- [ ] fix readme

far future goals
- [ ] turn to C++
- [ ] following that, explore atomicity and concurrency; possibly lock-free data structures?
- [ ] migrate from a sorted list with binary search in the memtable to a skip list (apparently adjacent to leveldb and rocksdb)

## data structure concepts used
LSM tree, database storage, hashing. Since a hash map is a very common data structure used in our homeworks and a database is a well-known tool in almost all apps and companies around the world, I wanted to learn about its implementation a bit more.
Binary search is used in the mem table (literally textbook binary search: the index bisects the list and then inserts if the index is equal to the necessary key in the memtable).

## project workflow
The major concepts here are the write-ahead log (WAL), memory table (MemTable), (SSTable), and the log-structured merge tree (LSM tree). We want persistence, fast access, and accurate sorting. 

### What's Write-Ahead Logging?
This is essentially keeping a journal of what happened and the changes that will happen BEFORE you apply it to the database. You can make them cute little diary entries. This helps ensure data persistence and recovery! This means that each operation (set, del) will need to log these entries in the WAL - this helps us practice modular programming as well as object oriented programming.

### Isn't this whole thing a "Memory Table?"
Not quite. While our database stores key-value pairs, we use Memory Tables (MemTables) to make our database's writes much faster, providing quick access to recently written data (almost like a cache or sorting tray).

Woah, what's this? the `bisect` library and `bisect_left()` - these are high level Python libraries and functions that allow us to insert values into a sorted list without constant re-sorting. Magically, it's O(logn) (because it uses a binary search to find the insertion point). Python is magic.

### All right, what's this LSM Tree you're on about?
This is a Log-Structured Merge tree, a data structure that efficiently stores and retrieves key-value pairs, particularly for high-write volumes. The LSM tree achieves this with a combination of in-memory storage (our temporary MemTables) and disk-based storage (when we flush the MemTables to the disk as an SSTable - an immutable on-disk storage format). Imagine you're in your office: new papers go in your inbox; when your inbox is full, you sort it and put it in a folder; when you have many folders, you put them into a box and merge them (compaction). 

### Okay, why are we threading? I thought this was just a database!
Hold on, we're just trying to synchronize data. First off, we're using **locks**: ensuring that only one thread can access a shared resource at a time. This comes with mutual exclusion (only one thread holds the lock at a time) and blocking behavior (threads will wait until lock is released if they try to acquire a locked lock). However, we're using an `RLock()`, a reentrant lock - a thread can acquire the same lock multiple times without causing deadlock (a thread may need to acquire a lock again while already holding the lock). 

###### ...What?
Okay, threading is a whole different thing. For now, we're trying to prevent race conditions and ensure thread safety. When we write to our database, we're going to test it rigorously with many threads (independent flows of control in a SINGLE program that share resources). 
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

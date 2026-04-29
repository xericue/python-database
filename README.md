# Write-Heavy Database in Python

project overview: this is a write-heavy database implemented from scratch in Python. No SQL or SQLite, just the implementation. 
- working KV storage engine
- write ahead log (WAL)
- MemTable
- SSTables for flushing to disk
- LSM-Tree (Log-Structured Merge Tree)
- Tombstone class to mark deleted keys
- persistent memory storage
- interactive CLI/REPL
- thread-safe

 while my initial goals for this project are silly (set "bruh" -> "gurt", set "dylan" -> "goat"), i hope to scale this in the future, possibly for high-frequency trading!


### How can I run this?
Copy the repository and just... Go. `make` will run it all for you. `make clean` to clean the database remnants and `make test` to see the unit tests in action.

# Checklist
- [x] implement sstable
- [x] implement memtable fully
- [x] implement the actual LSM tree
- [x] generate unit tests
- [x] personally try the database
- [x] record a video
- [x] fix readme

# Future Goals
- [ ] migrate from a sorted list with binary search in the memtable to a skip list (possible benchmarks against Google's LevelDB and Meta's RocksDB)
- [ ] more levels to the LSM tree
- [ ] convert to C++
- [ ] following that, explore atomicity and concurrency; possibly a lock-free data structure?
- [ ] write benchmark script (sets/gets/range at 1k, 10k, 100k entries)
- [ ] implement MVCC (multi-version concurrency control) - instead of locking on writes, create a new version of a key w/ timestamp; reads snapshot database
- [ ] look into database indexing?...

## Data Structure Concepts Used
- Hash maps: since a hash map is a very common data structure used in our homeworks and a database is a well-known tool in almost all apps and companies around the world, I wanted to learn about its implementation a bit more... Which is ultimately a database!
- Binary search: used in the mem table (literally textbook binary search: the index bisects the list and then inserts if the index is equal to the necessary key in the memtable).
- LSM-Tree: Lists and maintaining key-value pairs in memory

## Project Workflow
The major concepts here are the write-ahead log (WAL), memory table (MemTable), (SSTable), and the log-structured merge tree (LSM tree). We want persistence, fast access, and accurate sorting. 

- set through CLI -> WAL write and MemTable initialization
- if MemTable is full: flush into an SSTable, set a WAL checkpoint
- if too many SSTables - compact()

- get through CLI -> check MemTable
- if found - return from MemTable, continue CLI loop
- if not, go check the SSTables (icky disk reading)
- if not found at all, return None

### What's Write-Ahead Logging?
This is essentially keeping a journal of what happened and the changes that will happen BEFORE you apply it to the database. You can make them cute little diary entries. This helps ensure data persistence and recovery! This means that each operation (set, del) will need to log these entries in the WAL - this helps us practice modular programming as well as object oriented programming.

### Isn't this whole thing a "Memory Table?"
Not quite. While our database stores key-value pairs, we use Memory Tables (MemTables) to make our database's writes much faster, providing quick access to recently written data (almost like a cache or sorting tray).

Woah, what's this? the `bisect` library and `bisect_left()` - these are high level Python libraries and functions that allow us to insert values into a sorted list without constant re-sorting. Magically, it's O(logn) (because it uses a binary search to find the insertion point). Python is magic.

### All right, what's this LSM Tree you're on about?
This is a Log-Structured Merge tree, a data structure that efficiently stores and retrieves key-value pairs, particularly for high-write volumes. The LSM tree achieves this with a combination of in-memory storage (our temporary MemTables) and disk-based storage (when we flush the MemTables to the disk as an SSTable - an immutable on-disk storage format). Imagine you're in your office: new papers go in your inbox; when your inbox is full, you sort it and put it in a folder; when you have many folders, you put them into a box and merge them (compaction). 

#### Dude, why are we compacting? 
Because, imagine we stop our SSTables at, like, two keys each, and then we hit our maximum SSTables. LAME! We can compact them so that each compacted SSTable holds more key value pairs - starting it off slow just makes traversal easier when we have so many writes.

```
# Before compaction:
sstables: [
    sstable_0.db: [("apple", 1), ("banana", 2)],
    sstable_1.db: [("banana", 3), ("cherry", 4)],
    sstable_2.db: [("apple", 5), ("date", 6)]
]

# After compaction:
sstables: [
    sstable_compacted.db: [
        ("apple", 5),    # Latest value wins
        ("banana", 3),   # Latest value wins
        ("cherry", 4),
        ("date", 6) ]
    ]
```

#### Okay, why are we threading? I thought this was just a database!
Hold on, we're just trying to synchronize data. First off, we're using **locks**: ensuring that only one thread can access a shared resource at a time. This comes with mutual exclusion (only one thread holds the lock at a time) and blocking behavior (threads will wait until lock is released if they try to acquire a locked lock). However, we're using an `RLock()`, a reentrant lock - a thread can acquire the same lock multiple times without causing deadlock (a thread may need to acquire a lock again while already holding the lock). 

###### ...What?
Okay, threading is a whole different thing. For now, we're trying to prevent race conditions and ensure thread safety. When we write to our database, we're going to test it rigorously with many threads (independent flows of control in a SINGLE program that share resources). 

# Expected I/O
Input commands in the CLI (get set del range exit)

Output files in the repository with data that persists !!!

# Performance
In the main LSMTree, the `set` and `get` operations are O(n) (MemTable list comprehensions and SSTable look ups). Flushing MemTables to SSTables is O(n log n). A skip list will give us a true O(log n) instead of our O(n) because of our MemTable list comprehension, as, every time we have to search for an item, we rebuild the entries from scratch (`[k for k, _ in self.entries]`). It should be an O(log n) binary search, but it's really O(n) here.


# Challenges
The WAL, MemTable, and SSTable all interface with one another and build to create the LSM Tree at the end, which is quite difficult to keep track of. 

# Improvements
I'd love to implement this with a skiplist to practice concurrency as well as explore more threading. These two as well as the OOP of this practice naturally align well with C++, and I'd love to see how this could be fleshed out.

# Learning
Learned a lot about the internals of modern database engines and infrastructure! I had never thought that a database would actually interface with the OS to plant files inside of it (as we do here with the repository)... As I did a bit more research, I actually saw so many data structures and algorithms come to life to build the technologies we know today (AVL trees/any self-balancing tree being used for O(log n) get/set/del, binary search, many hash maps...).

# Real World Relevance
systems that require large volumes of data with strict latency requirements for writing more than they read (logging and monitoring systems, financial transaction). with my future implementations, i may start benchmarking against Google's LevelDB and Meta's RocksDB, which are production-ready databases that utilize these similar features. 

# Use of AI Tools
I generated unit tests after writing a few for each class. I also used it for general fact checking (misspelling variables/inconsistent variables). I did this throughout the project and committed/tested frequently, but some implicit errors snuck by me.
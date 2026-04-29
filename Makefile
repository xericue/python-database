# Makefile for LSM-tree database.
# Usage:
# make				-> run main db module
# make run			-> run main db module
# make test			-> run unit tests
# make test-v		-> run unit tests, verbose
# make clean		-> remove generated db files and python caches

PYTHON	:= python3
MAIN	:= db.py
TESTS	:= db_unit.py
DB_PATH := mydb

.PHONY: all run test test-v clean install help

all: run

run:
	$(PYTHON) $(MAIN)

test:
	$(PYTHON) -m unittest $(TESTS)

test-v:
	$(PYTHON) -m unittest -v $(TESTS)

clean:
	@echo "CLEANING GENERATED FILES UP!!!"
	rm -rf __pycache__ .pytest_cache $(DB_PATH)/
	find . -type f -name "*.pyc"  -delete
	find . -type f -name "*.pyo"  -delete
	find . -type f -name "*.tmp"  -delete
	find . -type f -name "*.log"  -delete
	find . -type f -name "*.pkl"  -delete
	find . -type f -name "*.dat"  -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
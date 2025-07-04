#!/bin/bash
set -e

echo "Resetting cat_facts.db..."

# Delete existing DB if it exists
rm -f cat_facts.db

# Run the Python script to load the DB
python3 import_cat_facts.py

# Keep running the container
exec "$@"
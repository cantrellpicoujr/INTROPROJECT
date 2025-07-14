#!/bin/bash

set -e

echo "Starting backend container..."
echo "Using BACKEND_PORT=${BACKEND_PORT}"
echo "Resetting cat_facts.db..."

# Delete existing DB if it exists
rm -f cat_facts.db

# Run the Python script to load the DB
python3 scripts/import_cat_facts.py

# Run passed command (like uvicorn) using exec
exec "$@"

import pytest
import sqlite3
import os

from services.db import get_all_catfacts, get_random_catfact, add_catfact_to_db, get_db_path

# Test database path.
TEST_DB_PATH = "test_cat_facts.db"

@pytest.fixture(autouse=True, scope="function")
def setup_and_teardown_db():
    """
    Pytest fixture to set up and tear down a test database for each test.

    """

    # Override the DB_PATH environment variable to use the test database.
    os.environ["DB_PATH"] = "test_cat_facts.db"

    # Connect to the test database.
    conn = sqlite3.connect("test_cat_facts.db")
    cursor = conn.cursor()

    # Drop the table if it exists to ensure a clean slate.
    cursor.execute("DROP TABLE IF EXISTS cat_facts")

    # Create the cat_facts table
    cursor.execute("""
        CREATE TABLE cat_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit changes and close the connection.
    conn.commit()
    conn.close()

    # Yield to run the test, then clean up after.
    yield

    # Remove the test database file after the test.
    os.remove("test_cat_facts.db")

def test_add_and_get_all_catfacts():
    """
    Test adding a cat fact and retrieving all facts from the database.
    """

    # The fact to add.
    fact_text = "Cats purr to communicate."

    # Add the fact to the DB.
    result = add_catfact_to_db(fact_text)

    # Check the returned fact matches.
    assert result["fact"] == fact_text

    # Retrieve all facts from the DB.
    all_facts = get_all_catfacts()

    # There should be exactly one fact.
    assert len(all_facts) == 1

    # The fact should match what was added.
    assert all_facts[0]["fact"] == fact_text

def test_get_random_catfact():
    """
    Test retrieving a random cat fact from multiple facts.

    """

    # Add multiple facts to the DB.
    facts = ["Cats sleep a lot.", "Cats can jump 6 times their length."] 

     # Facts to add.
    for f in facts:
        add_catfact_to_db(f)  

    # Get a random fact from the DB.
    random_fact = get_random_catfact() 

    # The returned fact should be one of the added facts. 
    assert random_fact in facts         

def test_add_empty_fact():
    """
    Test that adding an empty fact raises a ValueError.

    """

    # Try to add an empty fact (just spaces), should raise ValueError.
    with pytest.raises(ValueError, match="Fact cannot be empty."):
        add_catfact_to_db("   ")

def test_add_duplicate_fact():
    """
    Test that adding a duplicate fact raises a ValueError.

    """

     # Add a fact.git 
    add_catfact_to_db("Cats have whiskers.") 

    # Try to add the same fact again, should raise ValueError for duplicate.
    with pytest.raises(ValueError, match="Duplicate fact."):
        add_catfact_to_db("Cats have whiskers.")

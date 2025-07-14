import os
import random
import sqlite3
from typing import List

def get_db_path():
    """
    Get the path to the database file.
    
    """

    return os.getenv("DB_PATH", "cat_facts.db")

def get_all_catfacts() -> List[dict]:
    """
    Retrieve all cat facts from the database.

    Returns:
        List[dict]: A list of dictionaries containing cat fact data.

    """

    # Connect to the database.
    conn = sqlite3.connect(get_db_path())
    
    # Create a cursor object.
    cursor = conn.cursor()

    # Execute SQL to select all cat facts.
    cursor.execute("SELECT id, fact, created_at FROM cat_facts")

    # Fetch all rows from the query.
    rows = cursor.fetchall()

    # Close the database connection.
    conn.close()

    # Return a list of dictionaries for each cat fact.
    return [{"id": r[0], "fact": r[1], "created_at": r[2]} for r in rows]

def get_random_catfact() -> str:
    """
    Retrieve a random cat fact from the database.

    Returns:
        str: A random cat fact, or None if no facts exist.
    """

    # Connect to the database.
    conn = sqlite3.connect(get_db_path())

    # Create a cursor object.
    cursor = conn.cursor()

    # Execute SQL to select all facts.
    cursor.execute("SELECT fact FROM cat_facts")
    
    # Fetch all facts from the query.
    facts = [row[0] for row in cursor.fetchall()]

    # Close the database connection.
    conn.close()

    # Check if there are no facts and return None.
    if not facts:
        return None
    
    # Return a random fact from the list.
    return random.choice(facts)

def add_catfact_to_db(fact: str) -> dict:
    """
    Add a new cat fact to the database.

    Args:
        fact (str): The cat fact to add.

    Returns:
        dict: The newly added cat fact as a dictionary.

    """

    # Remove leading and trailing whitespace from the fact.
    fact = fact.strip()

    # Check if the fact is empty and raise an error.
    if not fact:
        raise ValueError("Fact cannot be empty.")

    # Connect to the database.
    conn = sqlite3.connect(get_db_path())

    # Set row factory to access columns by name.
    conn.row_factory = sqlite3.Row

    # Create a cursor object.
    cursor = conn.cursor()

    try:
        # Execute SQL to insert the new fact.
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))

        # Commit the transaction.
        conn.commit()

        # Get the ID of the newly inserted fact.
        new_id = cursor.lastrowid

        # Retrieve the complete record of the newly added fact.
        cursor.execute("SELECT * FROM cat_facts WHERE id = ?", (new_id,))
        new_fact = cursor.fetchone()

        # Return the new fact as a dictionary.
        return {
            "id": new_fact["id"],
            "fact": new_fact["fact"],
            "created_at": new_fact["created_at"],
        }
    
    except sqlite3.IntegrityError:
        raise ValueError("Duplicate fact.")
    
    finally:
        conn.close()
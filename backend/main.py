from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from pydantic import BaseModel
import random
import sqlite3

# Configure logging to file and console.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app.
app = FastAPI()

# Enable CORS for all origins (adjust for production).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path.
DB_PATH: str = "cat_facts.db"

# Pydantic model for responses.
class CatFact(BaseModel):
    id: int
    fact: str
    created_at: str

@app.get("/catfacts", response_model=list[CatFact])
def get_all_catfacts() -> list[dict]:
    """
    Fetch all cat facts from the database.

    Returns:
        list[dict]: A list of dictionaries, each representing a cat fact with keys:
                    'id' (int), 'fact' (str), and 'created_at' (str).
    """

    logger.info("Fetching all cat facts from the database.")

    # Connect to database.
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)

    # Connect to cursor object.
    cursor: sqlite3.Cursor = conn.cursor() 

    cursor.execute("SELECT id, fact, created_at FROM cat_facts")

    # Return all items
    rows = cursor.fetchall()

    # Close connection to database.
    conn.close()

    logger.info(f"Fetched {len(rows)} cat facts.")

    return [{"id": r[0], "fact": r[1], "created_at": r[2]} for r in rows]

@app.get("/catfacts/random")
def get_random_catfact() -> dict:
    """
    Fetch a random cat fact from the database.

    Returns:
        dict: A dictionary containing a single random cat fact, e.g., {"fact": "Cats sleep 70% of their lives"}.
    """


    logger.info("Fetching a random cat fact.")

    # Connect to database.
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)

    # Create cursor object.
    cursor: sqlite3.Cursor = conn.cursor()

    cursor.execute("SELECT fact FROM cat_facts")

    # Store all facts.
    facts: list = [row[0] for row in cursor.fetchall()]

    # Close connection to database.
    conn.close()

    if not facts:
        logger.warning("No cat facts available to return.")
        raise HTTPException(status_code=404, detail="No cat facts available")

    # Pick a random fact.
    fact: str = random.choice(facts)

    logger.info(f"Random cat fact selected: {fact}.")

    return {"fact": fact}

@app.post("/catfacts")
def add_catfact(fact: str = Form(...)) -> dict:
    """
    Add a new cat fact to the database.

    Args:
        fact (str): The cat fact submitted via form data.

    Returns:
        dict: The newly added cat fact with its ID and creation timestamp.
    """

    fact = fact.strip()

    logger.info(f"Attempting to add new cat fact: '{fact}'")

    if not fact:
        logger.warning("Attempted to add an empty fact.")
        raise HTTPException(status_code=400, detail="Fact cannot be empty.")
    
    # Connect to database.
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)

    # To access columns by name.
    conn.row_factory = sqlite3.Row 

    # Create cursor object.
    cursor: sqlite3.Cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))

        # Save to database.
        conn.commit()

        # Fetch the newly inserted row by last inserted id.
        new_id: int = cursor.lastrowid

        cursor.execute("SELECT * FROM cat_facts WHERE id = ?", (new_id,))

        new_fact = cursor.fetchone()

        logger.info(f"Added new cat fact with id {new_id}.")

        return {
            "id": new_fact["id"],
            "fact": new_fact["fact"],
            "created_at": new_fact["created_at"],
        }
    
    except sqlite3.IntegrityError:
        logger.warning(f"Duplicate fact attempted: '{fact}'")
        raise HTTPException(status_code=409, detail="Duplicate fact.")
    
    finally:
        conn.close()
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import random
import logging

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use [""] for local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH: str = "cat_facts.db"

# Pydantic model for responses
class CatFact(BaseModel):
    id: int
    fact: str
    created_at: str

@app.get("/catfacts", response_model=list[CatFact])
def get_all_catfacts() -> list[dict]:
    """
    Fetch all cat facts from the database.
    """
    logger.info("Fetching all cat facts from the database.")
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor() 
    cursor.execute("SELECT id, fact, created_at FROM cat_facts")
    rows = cursor.fetchall()
    conn.close()
    logger.info(f"Fetched {len(rows)} cat facts.")
    return [{"id": r[0], "fact": r[1], "created_at": r[2]} for r in rows]

@app.get("/catfacts/random")
def get_random_catfact() -> dict:
    """
    Fetch a random cat fact from the database.
    """
    logger.info("Fetching a random cat fact.")
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute("SELECT fact FROM cat_facts")
    facts: list = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not facts:
        logger.warning("No cat facts available to return.")
        raise HTTPException(status_code=404, detail="No cat facts available")

    fact: str = random.choice(facts)
    logger.info(f"Random cat fact selected: {fact}.")
    return {"fact": fact}

@app.post("/catfacts")
def add_catfact(fact: str = Form(...)) -> dict:
    """
    Add a new cat fact to the database.
    """
    fact = fact.strip()
    logger.info(f"Attempting to add new cat fact: '{fact}'")
    if not fact:
        logger.warning("Attempted to add an empty fact.")
        raise HTTPException(status_code=400, detail="Fact cannot be empty.")

    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # to access columns by name
    cursor: sqlite3.Cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))
        conn.commit()

        # Fetch the newly inserted row by last inserted ID
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
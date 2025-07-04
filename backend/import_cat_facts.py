import sqlite3
import requests
import logging

DB_NAME: str = "cat_facts.db"
FACTS_API: str = "https://catfact.ninja/fact"
FACT_COUNT: int = 5

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("import_cat_facts.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """Initialize the database and create the cat_facts table if it doesn't exist."""
    logger.info("Initializing the database and ensuring table exists.")
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cat_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE,
            created_at DATE DEFAULT (DATE('now'))
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

def fetch_fact() -> str:
    """Fetch a single cat fact from the external API."""
    logger.info(f"Fetching a cat fact from {FACTS_API}")
    try:
        response: requests.Response = requests.get(FACTS_API)
        response.raise_for_status()  # raises exception on error
        data: dict = response.json()
        fact: str = data["fact"]
        logger.info(f"Fetched fact: {fact}")
        return fact
    except Exception as e:
        logger.error(f"Failed to fetch cat fact: {e}")
        raise

def save_fact(fact: str) -> None:
    """Insert a cat fact into the database if it's not a duplicate."""
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    try:
        cur.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact,))
        conn.commit()
        logger.info(f"Inserted fact into database: {fact}")
        print(f"✅ Inserted: {fact}")
    except sqlite3.IntegrityError:
        logger.warning(f"Skipped duplicate fact: {fact}")
        print(f"⚠️ Skipped (duplicate): {fact}")
    finally:
        conn.close()

def main() -> None:
    """Main execution: initialize DB, fetch and save cat facts."""
    logger.info("Starting cat facts import process.")
    init_db()
    for i in range(FACT_COUNT):
        logger.info(f"Processing fact {i+1} of {FACT_COUNT}")
        try:
            fact: str = fetch_fact()
            save_fact(fact)
        except Exception as e:
            logger.error(f"Error processing fact {i+1}: {e}")
    logger.info("Cat facts import process completed.")

if __name__ == "__main__":
    main()
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel

from services.db import get_all_catfacts, get_random_catfact, add_catfact_to_db

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

# Define Pydantic model for cat fact responses.
class CatFact(BaseModel):
    id: int
    fact: str
    created_at: str

@app.get("/catfacts", response_model=list[CatFact], status_code=status.HTTP_200_OK)
def api_get_all_catfacts():
    """
    Retrieve all cat facts from the database and return them as a list.

    Returns:
        List[CatFact]: A list of cat fact objects.

    """

    # Log the action of fetching all cat facts.
    logger.info("Fetching all cat facts from the database.")

    # Return all cat facts from the database.
    return get_all_catfacts()

@app.get("/catfacts/random", status_code=status.HTTP_200_OK)
def api_get_random_catfact():
    """
    Retrieve a random cat fact from the database.

    Returns:
        dict: A dictionary containing a random cat fact.

    """

    # Log the action of fetching a random cat fact.
    logger.info("Fetching a random cat fact.")

    # Get a random cat fact from the database.
    fact = get_random_catfact()

    # Check if no cat facts are available and raise an error.
    if not fact:
        logger.warning("No cat facts available.")
        raise HTTPException(status_code=404, detail="No cat facts available")
    
    # Log the selected random cat fact.
    logger.info(f"Random cat fact selected: {fact}")

    # Return the random cat fact.
    return {"fact": fact}

@app.post("/catfacts", status_code=status.HTTP_201_CREATED)
def api_add_catfact(fact: str = Form(...)):
    """
    Add a new cat fact to the database.

    Args:
        fact (str): The cat fact to add.

    Returns:
        dict: The newly added cat fact as a dictionary.

    """

    # Log the attempt to add a new cat fact.
    logger.info(f"Attempting to add new cat fact: '{fact}'")

    try:
        # Add the cat fact to the database.
        return add_catfact_to_db(fact)
    
    except ValueError as ve:
        # Log the error if the fact is empty or a duplicate.
        logger.warning(str(ve))

        # Set the status code based on the error type.
        status_code = 400 if "empty" in str(ve).lower() else 409

        # Raise an HTTPException with the appropriate status code and error message.
        raise HTTPException(status_code=status_code, detail=str(ve))

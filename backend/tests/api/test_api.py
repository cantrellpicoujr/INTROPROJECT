from fastapi.testclient import TestClient
import os
import pytest
import sqlite3

from main import app

# Create a test client for the FastAPI app.
client = TestClient(app)

# Define the path for the test database.
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

    # Create a cursor object.
    cursor = conn.cursor()

    # Drop the table if it exists to ensure a clean slate.
    cursor.execute("DROP TABLE IF EXISTS cat_facts")

    # Create the cat_facts table.
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

def test_get_all_catfacts():
    """
    Test retrieving all cat facts from the API.

    """

    # Send a GET request to the /catfacts endpoint.
    response = client.get("/catfacts")

    # Assert that the response status code is 200.
    assert response.status_code == 200

    # Assert that the response JSON is a list.
    assert isinstance(response.json(), list)

def test_add_and_get_random_catfact():
    """
    Test adding a new cat fact and retrieving a random cat fact from the API.

    """

    # Define the fact to add.
    fact = "Cats land on their feet."

    # Send a POST request to add the new fact.
    post_response = client.post("/catfacts", data={"fact": fact})

    # Assert that the response status code is 201.
    assert post_response.status_code == 201

    # Get the response data as JSON.
    data = post_response.json()

    # Assert that the returned fact matches the added fact.
    assert data["fact"] == fact

    # Send a GET request to retrieve a random cat fact.
    get_response = client.get("/catfacts/random")

    # Assert that the response status code is 200.
    assert get_response.status_code == 200

    # Assert that the response JSON contains the "fact" key.
    assert "fact" in get_response.json()

def test_add_empty_fact():
    """
    Test that adding an empty fact returns a 400 error.

    """

    # Send a POST request with an empty fact.
    response = client.post("/catfacts", data={"fact": "   "})

    # Assert that the response status code is 400.
    assert response.status_code == 400

    # Assert that the error message contains "Fact cannot be empty".
    assert "Fact cannot be empty" in response.json()["detail"]

def test_add_duplicate_fact():
    """
    Test that adding a duplicate fact returns a 409 error.

    """

    # Define the fact to add.
    fact = "Cats can rotate their ears 180 degrees."

    # Send a POST request to add the fact.
    client.post("/catfacts", data={"fact": fact})

    # Send another POST request with the same fact.
    response = client.post("/catfacts", data={"fact": fact})

    # Assert that the response status code is 409.
    assert response.status_code == 409
    print(response.status_code == 409)

    # Assert that the error message contains "Duplicate fact".
    assert "Duplicate fact" in response.json()["detail"]
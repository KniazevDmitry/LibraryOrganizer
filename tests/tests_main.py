import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Define the absolute path for the test database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'test.db')}"

# Create an engine and session for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency override to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Create a book
book_data = {
    "title": "Blindsight",
    "author": "Peter Watts",
    "description": "The novel explores themes of identity, consciousness, free will, artificial intelligence, "
                   "neurology, and game theory as well as evolution and biology."
}
book_response = client.post("/books/", json=book_data)
created_book = book_response.json()


def test_book_created():
    assert book_response.status_code == 200

    # Remove the 'id' field for comparison
    created_book_data = {k: v for k, v in created_book.items() if k != 'id'}

    assert created_book_data == book_data


def test_book_deleted():
    book_id = created_book["id"]
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200

    get_deleted_response = client.get(f"/books/{book_id}")
    assert get_deleted_response.status_code == 404

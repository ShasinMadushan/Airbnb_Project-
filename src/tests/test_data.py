import duckdb
import pytest
import os

# Define the path to your database
DB_PATH = "data/processed/airbnb.duckdb"

@pytest.fixture
def db_connection():
    """Establishes a temporary connection to the database for testing."""
    con = duckdb.connect(DB_PATH, read_only=True)
    yield con
    con.close()

def test_database_exists():
    """Check if the ELT pipeline successfully created the database file."""
    assert os.path.exists(DB_PATH), "Database file does not exist!"

def test_listings_table_has_data(db_connection):
    """Check if the listings table was populated."""
    result = db_connection.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    assert result > 0, "The listings table is empty!"

def test_no_negative_prices(db_connection):
    """Business Logic Check: Airbnb prices cannot be negative."""
    result = db_connection.execute("SELECT COUNT(*) FROM listings WHERE price < 0").fetchone()[0]
    assert result == 0, f"Found {result} records with negative prices!"

def test_primary_key_uniqueness(db_connection):
    """Engineering Check: Ensure the listing ID is completely unique."""
    total_rows = db_connection.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    distinct_ids = db_connection.execute("SELECT COUNT(DISTINCT id) FROM listings").fetchone()[0]
    assert total_rows == distinct_ids, "Duplicate Primary Keys found in the listings table!"
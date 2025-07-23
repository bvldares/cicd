import pytest
import sqlite3
import tempfile
import os
from fastapi.testclient import TestClient
from src.main import app
from src.db.database import get_db_connection


@pytest.fixture(scope="session")
def test_db():
    """Crea un database temporaneo per i test"""
    # Crea un file temporaneo per il database di test
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Modifica temporaneamente il path del database
    import src.db.database as db_module
    original_db_file = db_module.DATABASE_FILE
    db_module.DATABASE_FILE = db_path
    
    # Crea le tabelle nel database di test
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_on DATETIME
        )
    ''')
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    db_module.DATABASE_FILE = original_db_file


@pytest.fixture
def client(test_db):
    """Client di test per FastAPI"""
    return TestClient(app)


@pytest.fixture
def sample_todo_data():
    """Dati di esempio per i test"""
    return {
        "name": "Test Todo Item"
    }


@pytest.fixture
def db_connection(test_db):
    """Connessione al database di test"""
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

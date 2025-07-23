import pytest
import sqlite3
from src.db.database import get_db_connection, create_tables


def test_get_db_connection(test_db):
    """Test per verificare che la connessione al database funzioni"""
    conn = get_db_connection()
    assert conn is not None
    
    # Verifica che sia configurato con row_factory
    assert conn.row_factory == sqlite3.Row
    
    conn.close()


def test_database_tables_exist(db_connection):
    """Test per verificare che le tabelle esistano"""
    cursor = db_connection.cursor()
    
    # Verifica che la tabella todo esista
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='todo'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "todo"


def test_insert_todo_item(db_connection):
    """Test per inserire un todo item nel database"""
    cursor = db_connection.cursor()
    
    # Inserisci un item
    cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Test Item",))
    db_connection.commit()
    
    # Verifica che sia stato inserito
    cursor.execute("SELECT * FROM todo WHERE name = ?", ("Test Item",))
    result = cursor.fetchone()
    
    assert result is not None
    assert result["name"] == "Test Item"
    assert result["id"] is not None
    assert result["created_on"] is not None


def test_select_todo_items(db_connection):
    """Test per selezionare todo items dal database"""
    cursor = db_connection.cursor()
    
    # Inserisci alcuni items
    cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Item 1",))
    cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Item 2",))
    db_connection.commit()
    
    # Seleziona tutti gli items
    cursor.execute("SELECT * FROM todo ORDER BY id")
    results = cursor.fetchall()
    
    assert len(results) == 2
    assert results[0]["name"] == "Item 1"
    assert results[1]["name"] == "Item 2"


def test_delete_todo_item(db_connection):
    """Test per eliminare un todo item dal database"""
    cursor = db_connection.cursor()
    
    # Inserisci un item
    cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Item to Delete",))
    db_connection.commit()
    
    # Ottieni l'ID dell'item
    cursor.execute("SELECT id FROM todo WHERE name = ?", ("Item to Delete",))
    item_id = cursor.fetchone()["id"]
    
    # Elimina l'item
    cursor.execute("DELETE FROM todo WHERE id = ?", (item_id,))
    db_connection.commit()
    
    # Verifica che sia stato eliminato
    cursor.execute("SELECT * FROM todo WHERE id = ?", (item_id,))
    result = cursor.fetchone()
    assert result is None


def test_unique_constraint(db_connection):
    """Test per verificare il vincolo di unicità sui nomi"""
    cursor = db_connection.cursor()
    
    # Inserisci un item
    cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Unique Item",))
    db_connection.commit()
    
    # Prova a inserire lo stesso nome
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO todo (name) VALUES (?)", ("Unique Item",))
        db_connection.commit()

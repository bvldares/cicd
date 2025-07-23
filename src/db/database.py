import sqlite3
import os


# Path del database relativo alla root del progetto
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'my_api.db')

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"Errore durante la connessione al database: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    try:
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
        print("Tabelle create o già esistenti.")
    except sqlite3.Error as e:
        print(f"Errore nella creazione delle tabelle: {e}")
    finally:
        conn.close()


# Inizializza le tabelle quando il modulo viene importato
if __name__ == "__main__":
    create_tables()

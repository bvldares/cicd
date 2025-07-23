from fastapi import APIRouter, Path, HTTPException
from typing import List
from ..db.database import get_db_connection
from ..models.todo import TodoItem, TodoItemResponse, TodoItemCreate, DeleteResponse, ErrorResponse

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoItemResponse])
def get_todos():
    """Recupera tutti i todo items"""
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo ORDER BY id")
        rows = cursor.fetchall()
        
        # Converte i risultati in formato dizionario per Pydantic
        todos = []
        for row in rows:
            todos.append({
                "id": row["id"],
                "name": row["name"],
                "created_on": row["created_on"],
                "completed_on": row["completed_on"]
            })
        
        return todos
    except Exception as e:
        print(f"Errore nel recupero dei todos: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving todos")
    finally:
        conn.close()


@router.post("/", response_model=dict)
def add_item(item: TodoItemCreate):
    """Aggiunge un nuovo todo item"""
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO todo (name) VALUES (?)"
        cursor.execute(sql, (item.name,))
        conn.commit()
        
        return {"message": "Todo item added successfully"}
    except Exception as e:
        print(f"Errore nell'inserimento: {e}")
        raise HTTPException(status_code=500, detail="Error adding todo item")
    finally:
        conn.close()


@router.delete("/{item_id}", response_model=dict)
def delete_item(item_id: int = Path(..., title="The ID of the item to delete")):
    """Elimina un todo item"""
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Verifica se l'item esiste
        cursor.execute("SELECT id FROM todo WHERE id = ?", (item_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Todo item not found")
        
        # Elimina l'item
        sql = "DELETE FROM todo WHERE id = ?"
        cursor.execute(sql, (item_id,))
        conn.commit()
        
        return {"message": f"Todo item with id {item_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Errore nella cancellazione: {e}")
        raise HTTPException(status_code=500, detail="Error deleting todo item")
    finally:
        conn.close()

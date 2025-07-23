from fastapi import FastAPI, Path
from database import get_db_connection
from pydantic import BaseModel
 

app = FastAPI()

@app.get("/")
def get_todos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo ORDER BY id")
        rows = cursor.fetchall()

        return rows
    except Exception as e: 
        print(e)
    finally:
        conn.close()
        



class TodoItem(BaseModel):
    name: str


@app.post("/items")
def add_item(item: TodoItem):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql= "INSERT INTO todo (name) VALUES (?)"

        cursor.execute(sql, (item.name,))
        conn.commit()

        return {"message": "Todo item added successfully"}
    
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        conn.close()


@app.delete("/deleteItem/{item_id}")
def delete_item(item_id: int = Path(..., title="The ID of the item to delete")):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM todo WHERE id = ?"

        cursor.execute(sql, (item_id,))

        conn.commit()

        return {"message": f"Todo item with id {item_id} deleted successfully"}
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        conn.close()
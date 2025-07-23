import pytest
from fastapi.testclient import TestClient


def test_get_todos_empty(client):
    """Test per ottenere todo quando la lista è vuota"""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_add_todo_item(client, sample_todo_data):
    """Test per aggiungere un nuovo todo item"""
    response = client.post("/todos/", json=sample_todo_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Todo item added successfully"


def test_get_todos_with_items(client, sample_todo_data):
    """Test per ottenere todo dopo aver aggiunto un item"""
    # Aggiungi un item
    client.post("/todos/", json=sample_todo_data)
    
    # Ottieni tutti i todo
    response = client.get("/todos/")
    assert response.status_code == 200
    
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["name"] == sample_todo_data["name"]
    assert "id" in todos[0]
    assert "created_on" in todos[0]


def test_delete_todo_item(client, sample_todo_data):
    """Test per eliminare un todo item"""
    # Aggiungi un item
    client.post("/todos/", json=sample_todo_data)
    
    # Ottieni l'ID dell'item
    response = client.get("/todos/")
    todo_id = response.json()[0]["id"]
    
    # Elimina l'item
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Todo item with id {todo_id} deleted successfully"
    
    # Verifica che l'item sia stato eliminato
    response = client.get("/todos/")
    assert response.json() == []


def test_delete_nonexistent_item(client):
    """Test per eliminare un item che non esiste"""
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo item not found"


def test_add_duplicate_todo_item(client, sample_todo_data):
    """Test per aggiungere un todo item duplicato"""
    # Aggiungi il primo item
    response1 = client.post("/todos/", json=sample_todo_data)
    assert response1.status_code == 200
    
    # Prova ad aggiungere lo stesso item
    response2 = client.post("/todos/", json=sample_todo_data)
    assert response2.status_code == 500  # Dovrebbe fallire per vincolo UNIQUE


def test_add_invalid_todo_item(client):
    """Test per aggiungere un todo item con dati non validi"""
    response = client.post("/todos/", json={})
    assert response.status_code == 422  # Validation error


def test_root_endpoint(client):
    """Test per l'endpoint root"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo API is running!"

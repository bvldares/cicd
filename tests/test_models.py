import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models.todo import TodoItem, TodoItemResponse, TodoItemCreate


def test_todo_item_creation():
    """Test per creare un TodoItem"""
    item = TodoItem(name="Test Item")
    assert item.name == "Test Item"


def test_todo_item_create():
    """Test per creare un TodoItemCreate"""
    item = TodoItemCreate(name="New Item")
    assert item.name == "New Item"


def test_todo_item_response():
    """Test per creare un TodoItemResponse"""
    now = datetime.now()
    item = TodoItemResponse(
        id=1,
        name="Response Item",
        created_on=now,
        completed_on=None
    )
    
    assert item.id == 1
    assert item.name == "Response Item"
    assert item.created_on == now
    assert item.completed_on is None


def test_todo_item_validation_error():
    """Test per verificare gli errori di validazione"""
    # Test: campo name mancante
    with pytest.raises(ValidationError):
        TodoItem()  # Manca il campo name
    
    # Test: campo name vuoto
    with pytest.raises(ValidationError):
        TodoItem(name="")  # Nome vuoto non valido
    
    # Test: campo name con solo spazi
    with pytest.raises(ValidationError):
        TodoItem(name="   ")  # Solo spazi non valido


def test_todo_item_response_with_completion():
    """Test per TodoItemResponse con data di completamento"""
    now = datetime.now()
    completed = datetime.now()
    
    item = TodoItemResponse(
        id=1,
        name="Completed Item",
        created_on=now,
        completed_on=completed
    )
    
    assert item.completed_on == completed


def test_todo_item_json_serialization():
    """Test per la serializzazione JSON"""
    item = TodoItem(name="Serializable Item")
    json_data = item.model_dump()
    
    assert json_data == {"name": "Serializable Item"}


def test_todo_item_from_dict():
    """Test per creare TodoItem da dizionario"""
    data = {"name": "Dict Item"}
    item = TodoItem(**data)
    
    assert item.name == "Dict Item"

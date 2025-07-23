from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoItem(BaseModel):
    name: str


class TodoItemResponse(BaseModel):
    id: int
    name: str
    created_on: datetime
    completed_on: Optional[datetime] = None


class TodoItemCreate(BaseModel):
    name: str


class DeleteResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str

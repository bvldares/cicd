from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class TodoItem(BaseModel):
    name: str = Field(..., min_length=1, description="Nome del todo item (non può essere vuoto)")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Il nome non può essere vuoto o contenere solo spazi')
        return v.strip()


class TodoItemResponse(BaseModel):
    id: int
    name: str
    created_on: datetime
    completed_on: Optional[datetime] = None


class TodoItemCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nome del todo item (non può essere vuoto)")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Il nome non può essere vuoto o contenere solo spazi')
        return v.strip()


class DeleteResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str

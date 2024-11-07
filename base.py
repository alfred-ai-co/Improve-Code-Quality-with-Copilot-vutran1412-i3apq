from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class KanbanStatus(BaseModel):
    id: int
    name: str
    order: int

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v

    @field_validator('order')
    def order_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Order must be a positive integer')
        return v

class KanbanBoard(BaseModel):
    id: int
    name: str
    statuses: List[KanbanStatus]

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v

    @field_validator('statuses')
    def statuses_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Statuses must not be empty')
        return v

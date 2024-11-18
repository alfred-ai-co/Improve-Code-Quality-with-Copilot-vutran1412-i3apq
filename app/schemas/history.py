from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class HistoryEntry(BaseModel):
    """
    Represents an entry in the history log.

    Attributes:
        id (int): The unique identifier of the history entry.
        entity_type (str): The type of the entity.
        entity_id (int): The unique identifier of the entity.
        change_type (str): The type of change.
        timestamp (datetime): The timestamp of the change.
        user_id (int): The unique identifier of the user who made the change.
        details (Optional[str]): Optional details about the change.
    """
    id: int
    entity_type: str
    entity_id: int
    change_type: str
    timestamp: datetime
    user_id: int
    details: Optional[str] = Field(None, description="Optional details about the change")

    class Config:
        orm_mode = True

    def __repr__(self) -> str:
        return f"<HistoryEntry(id={self.id}, entity_type={self.entity_type})>"

class HistoryCreate(BaseModel):
    """
    Schema for creating a new history entry.

    Attributes:
        entity_type (str): The type of the entity.
        entity_id (int): The unique identifier of the entity.
        change_type (str): The type of change.
        user_id (int): The unique identifier of the user who made the change.
        details (Optional[str]): Optional details about the change.
    """
    entity_type: str
    entity_id: int
    change_type: str
    user_id: int
    details: Optional[str] = Field(None, description="Optional details about the change")

    class Config:
        orm_mode = True

class HistoryResponse(BaseModel):
    """
    Schema for the response of a history entry.

    Attributes:
        id (int): The unique identifier of the history entry.
        entity_type (str): The type of the entity.
        entity_id (int): The unique identifier of the entity.
        change_type (str): The type of change.
        timestamp (datetime): The timestamp of the change.
        user_id (int): The unique identifier of the user who made the change.
        details (Optional[str]): Optional details about the change.
    """
    id: int
    entity_type: str
    entity_id: int
    change_type: str
    timestamp: datetime
    user_id: int
    details: Optional[str] = Field(None, description="Optional details about the change")

    class Config:
        orm_mode = True

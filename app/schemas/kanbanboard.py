from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class KanbanBoardBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)

class KanbanBoardCreate(KanbanBoardBase):
    pass

class KanbanBoardUpdate(KanbanBoardBase):
    pass

class KanbanBoardInDB(KanbanBoardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class KanbanBoardResponse(KanbanBoardInDB):
    pass

class KanbanBoard(KanbanBoardInDB):
    tasks: List[str] = Field(default_factory=list, description="List of task IDs associated with the board")

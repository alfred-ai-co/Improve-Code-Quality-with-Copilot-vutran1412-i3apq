from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.history import HistoryEntry  # Corrected import statement


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str
    description: str
    kanban_board_id: int  # Ensure this field is required

    def __repr__(self) -> str:
        return f"<ProjectCreate(name={self.name}, description={self.description}, kanban_board_id={self.kanban_board_id})>"

class Project(BaseModel):
    """Schema for a project."""
    id: int
    name: str
    description: str
    kanban_board_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, description={self.description}, kanban_board_id={self.kanban_board_id}, created_at={self.created_at}, updated_at={self.updated_at})>"

class ProjectResponse(Project):
    """Schema for project response."""
    pass

    def __repr__(self) -> str:
        return f"<ProjectResponse(id={self.id}, name={self.name}, description={self.description}, kanban_board_id={self.kanban_board_id}, created_at={self.created_at}, updated_at={self.updated_at})>"

class ProjectWithHistory(Project):
    """Schema for a project with history entries."""
    history: List[HistoryEntry]

    def __repr__(self) -> str:
        return f"<ProjectWithHistory(id={self.id}, name={self.name}, description={self.description}, kanban_board_id={self.kanban_board_id}, created_at={self.created_at}, updated_at={self.updated_at}, history={self.history})>"

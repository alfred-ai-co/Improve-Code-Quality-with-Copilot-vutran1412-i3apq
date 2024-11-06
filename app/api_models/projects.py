from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProjectCreate(BaseModel):
    """
    Schema for creating a new project.
    """
    name: str
    description: Optional[str] = None

class ProjectResponse(ProjectCreate):
    """
    Schema for the response of a project.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

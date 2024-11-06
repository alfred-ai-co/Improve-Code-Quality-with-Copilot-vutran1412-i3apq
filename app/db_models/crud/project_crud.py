from sqlalchemy.orm import Session
from sqlalchemy import select  # Correct the import
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import Project

class ProjectCRUD(BaseCRUD):
    """
    CRUD operations for Project model.
    """
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def get_all(self, skip: int = 0, limit: int = 10):
        """
        Retrieve all projects with pagination.
        """
        result = self.db.execute(
            select(Project).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def get(self, id: int):
        """
        Retrieve a project by its ID.
        """
        result = self.db.execute(
            select(Project).filter(Project.id == id)
        )
        return result.scalars().one_or_none()

    def create(self, **kwargs):
        """
        Create a new project.
        """
        if 'kanban_board_id' not in kwargs or kwargs['kanban_board_id'] is None:
            raise ValueError("kanban_board_id cannot be None")
        return super().create(**kwargs)

    def update(self, id: int, **kwargs):
        """
        Update an existing project.
        """
        db_project = self.get(id)
        if db_project:
            for key, value in kwargs.items():
                setattr(db_project, key, value)
            self.db.commit()
            self.db.refresh(db_project)
        return db_project

    def delete(self, id: int):
        """
        Delete a project by its ID.
        """
        db_project = self.get(id)
        if db_project:
            self.db.delete(db_project)
            self.db.commit()
        return db_project

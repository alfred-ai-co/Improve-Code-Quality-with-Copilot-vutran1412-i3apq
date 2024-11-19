from sqlalchemy.orm import Session
from sqlalchemy import select  # Correct the import
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import Project, History
from app.db_models.crud.history_crud import HistoryCRUD

class ProjectCRUD(BaseCRUD):
    """
    CRUD operations for Project model.
    """
    def __init__(self, db: Session):
        """
        Initialize ProjectCRUD with a database session and HistoryCRUD instance.

        :param db: SQLAlchemy Session object.
        """
        super().__init__(db, Project)
        self.history_crud = HistoryCRUD(db)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Project]:
        """
        Retrieve all projects with pagination.

        :param skip: Number of records to skip.
        :param limit: Maximum number of records to return.
        :return: List of Project objects.
        """
        result = self.db.execute(
            select(Project).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def get(self, id: int) -> Optional[Project]:
        """
        Retrieve a project by its ID.

        :param id: Project ID.
        :return: Project object or None if not found.
        """
        result = self.db.execute(
            select(Project).filter(Project.id == id)
        )
        return result.scalars().one_or_none()

    def create(self, **kwargs: Dict[str, Any]) -> Project:
        """
        Create a new project.

        :param kwargs: The attributes of the project to create.
        :return: The created project.
        :raises ValueError: If 'kanban_board_id' is not provided or is None.
        :raises SQLAlchemyError: If there is an error during the creation process.
        """
        if 'kanban_board_id' not in kwargs or kwargs['kanban_board_id'] is None:
            raise ValueError("kanban_board_id cannot be None")
        return super().create(**kwargs)

    def update(self, id: int, **kwargs: Dict[str, Any]) -> Project:
        """
        Update an existing project.

        :param id: Project ID.
        :param kwargs: Attributes to update.
        :return: Updated Project object.
        :raises ValueError: If the project is not found.
        """
        db_project = self.get(id)
        if not db_project:
            raise ValueError("Project not found")
        for key, value in kwargs.items():
            setattr(db_project, key, value)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete(self, id: int) -> Optional[Project]:
        """
        Delete a project by its ID.

        :param id: Project ID.
        :return: Deleted Project object or None if not found.
        :raises ValueError: If the project is not found.
        """
        db_project = self.get(id)
        if not db_project:
            raise ValueError("Project not found")
        self.db.delete(db_project)
        self.db.commit()
        return db_project

    def update_status(self, project_id: int, new_status: str, user_id: int) -> Project:
        """
        Update the status of a project and create a history entry.

        :param project_id: The ID of the project to update.
        :param new_status: The new status of the project.
        :param user_id: The ID of the user making the change.
        :return: The updated project.
        :raises SQLAlchemyError: If there is an error during the update process.
        """
        try:
            project = self.get(project_id)
            if not project:
                raise ValueError("Project not found")
            project.status = new_status
            self.db.commit()
            self.db.refresh(project)

            # Add to history
            self.history_crud.create(
                entity_type="project",
                entity_id=project_id,
                change_type="status_change",
                user_id=user_id,
                details=f"Status changed to {new_status}"
            )
            return project
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError("Error updating project status") from e

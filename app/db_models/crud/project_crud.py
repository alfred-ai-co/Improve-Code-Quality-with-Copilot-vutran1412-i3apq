from sqlalchemy.orm import Session
from sqlalchemy import select  # Correct the import
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import Project

class ProjectCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def get_all(self, skip: int = 0, limit: int = 10):
        result = self.db.execute(
            select(Project).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def get(self, id: int):
        result = self.db.execute(
            select(Project).filter(Project.id == id)
        )
        return result.scalars().one_or_none()

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, id: int, **kwargs):
        db_project = self.get(id)
        if db_project:
            for key, value in kwargs.items():
                setattr(db_project, key, value)
            self.db.commit()
            self.db.refresh(db_project)
        return db_project

    def delete(self, id: int):
        db_project = self.get(id)
        if db_project:
            self.db.delete(db_project)
            self.db.commit()
        return db_project

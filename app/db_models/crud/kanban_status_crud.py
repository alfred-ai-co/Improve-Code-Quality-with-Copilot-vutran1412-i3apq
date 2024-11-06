from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import KanbanStatus

class KanbanStatusCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)

    def get_all(self, skip: int = 0, limit: int = 10):
        result = self.db.execute(
            select(KanbanStatus).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def get(self, id: int):
        result = self.db.execute(
            select(KanbanStatus).filter(KanbanStatus.id == id)
        )
        return result.scalars().one_or_none()

    def create(self, kanban_status: KanbanStatus):
        self.db.add(kanban_status)
        self.db.commit()
        self.db.refresh(kanban_status)
        return kanban_status

    def update(self, id: int, **kwargs):
        db_kanban_status = self.get(id)
        if db_kanban_status:
            for key, value in kwargs.items():
                setattr(db_kanban_status, key, value)
            self.db.commit()
            self.db.refresh(db_kanban_status)
        return db_kanban_status

    def delete(self, id: int):
        db_kanban_status = self.get(id)
        if db_kanban_status:
            self.db.delete(db_kanban_status)
            self.db.commit()
        return db_kanban_status

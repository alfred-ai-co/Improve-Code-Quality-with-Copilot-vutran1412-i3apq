from sqlalchemy.orm import Session
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import KanbanBoard

class KanbanBoardCRUD(BaseCRUD):
    """
    CRUD operations for KanbanBoard model.
    """
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)

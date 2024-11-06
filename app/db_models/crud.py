from sqlalchemy.orm import Session
from app.db_models.crud.base_crud import BaseCRUD, CRUDInterface
from app.db_models.crud.project_crud import ProjectCRUD
from app.db_models.crud.ticket_crud import TicketCRUD
from app.db_models.crud.kanban_board_crud import KanbanBoardCRUD
from app.db_models.crud.kanban_status_crud import KanbanStatusCRUD


class CRUDInterface(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, id: int, **kwargs):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class BaseCRUD(CRUDInterface):
    """Base CRUD class for all models"""
    def __init__(self, db: Session, model=None):
        self.db = db
        self.model = model

    def create(self, **kwargs):
        item = self.model(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def update(self, id: int, **kwargs):
        item = self.get(id)
        for key, value in kwargs.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: int):
        item = self.get(id)
        self.db.delete(item)
        self.db.commit()


class ProjectCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def create(self, **kwargs):
        if 'kanban_board_id' not in kwargs or kwargs['kanban_board_id'] is None:
            raise ValueError("kanban_board_id cannot be None")
        return super().create(**kwargs)


class TicketCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Ticket)


class KanbanBoardCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)


class KanbanStatusCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)

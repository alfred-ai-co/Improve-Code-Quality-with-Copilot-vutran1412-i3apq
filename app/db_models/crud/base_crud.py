from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class CRUDInterface(ABC):
    """
    Interface for CRUD operations.
    """
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
    """
    Base CRUD class for all models.
    """
    def __init__(self, db: Session, model=None):
        self.db = db
        self.model = model

    def create(self, **kwargs):
        """
        Create a new record.
        """
        item = self.model(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, id: int):
        """
        Retrieve a record by its ID.
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        """
        Retrieve all records.
        """
        return self.db.query(self.model).all()

    def update(self, id: int, **kwargs):
        """
        Update an existing record.
        """
        item = self.get(id)
        for key, value in kwargs.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: int):
        """
        Delete a record by its ID.
        """
        item = self.get(id)
        self.db.delete(item)
        self.db.commit()

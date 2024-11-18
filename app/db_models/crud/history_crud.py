from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db_models.base import History
from typing import List, Optional, Generator
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class HistoryCRUD:
    """
    CRUD operations for History model.
    """
    def __init__(self, db: Session):
        self.db = db

    @contextmanager
    def session_scope(self) -> Generator[None, None, None]:
        """
        Provide a transactional scope around a series of operations.
        """
        try:
            yield
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            self.db.close()

    def create(self, **kwargs) -> History:
        """
        Create a new history entry.
        """
        with self.session_scope():
            item = History(**kwargs)
            self.db.add(item)
            self.db.flush()  # Ensure the item is flushed to the session
            self.db.refresh(item)
            return item

    def get(self, id: int) -> Optional[History]:
        """
        Retrieve a history entry by its ID.
        """
        try:
            return self.db.query(History).filter(History.id == id).one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise

    def get_by_entity_id(self, entity_type: str, entity_id: int, skip: int = 0, limit: int = 10) -> List[History]:
        """
        Retrieve history entries by entity type and entity ID with pagination.
        """
        try:
            return self.db.query(History).filter(History.entity_type == entity_type, History.entity_id == entity_id).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise

    def update(self, id: int, **kwargs) -> History:
        """
        Update an existing history entry.
        """
        with self.session_scope():
            item = self.get(id)
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.flush()  # Ensure the item is flushed to the session
            self.db.refresh(item)
            return item

    def delete(self, id: int) -> History:
        """
        Delete a history entry by its ID.
        """
        with self.session_scope():
            item = self.get(id)
            self.db.delete(item)
            self.db.flush()  # Ensure the item is flushed to the session
            return item

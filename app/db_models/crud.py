from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db_models.base import Project, Ticket, KanbanBoard, KanbanStatus


class BaseCRUD:
    """
    Base CRUD class for all models.
    """
    def __init__(self, db: Session, model=None):
        self.db = db
        self.model = model

    def create(self, **kwargs):
        """
        Create a new record.

        :param kwargs: The attributes of the record to create.
        :return: The created record.
        :raises SQLAlchemyError: If there is an error during the creation process.
        """
        try:
            item = self.model(**kwargs)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get(self, id: int):
        """
        Retrieve a record by its ID.

        :param id: The ID of the record to retrieve.
        :return: The retrieved record or None if not found.
        :raises SQLAlchemyError: If there is an error during the retrieval process.
        """
        try:
            return self.db.query(self.model).filter(self.model.id == id).one_or_none()
        except SQLAlchemyError as e:
            raise e

    def get_all(self):
        """
        Retrieve all records.

        :return: A list of all records.
        :raises SQLAlchemyError: If there is an error during the retrieval process.
        """
        try:
            return self.db.query(self.model).all()
        except SQLAlchemyError as e:
            raise e

    def update(self, id: int, **kwargs):
        """
        Update an existing record.

        :param id: The ID of the record to update.
        :param kwargs: The attributes to update.
        :return: The updated record.
        :raises SQLAlchemyError: If there is an error during the update process.
        """
        try:
            item = self.get(id)
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, id: int):
        """
        Delete a record by its ID.

        :param id: The ID of the record to delete.
        :return: The deleted record.
        :raises SQLAlchemyError: If there is an error during the deletion process.
        """
        try:
            item = self.get(id)
            self.db.delete(item)
            self.db.commit()
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e


class ProjectCRUD(BaseCRUD):
    """
    CRUD operations for Project model.
    """
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def create(self, **kwargs):
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


class TicketCRUD(BaseCRUD):
    """
    CRUD operations for Ticket model.
    """
    def __init__(self, db: Session):
        super().__init__(db, Ticket)


class KanbanBoardCRUD(BaseCRUD):
    """
    CRUD operations for KanbanBoard model.
    """
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)


class KanbanStatusCRUD(BaseCRUD):
    """
    CRUD operations for KanbanStatus model.
    """
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)

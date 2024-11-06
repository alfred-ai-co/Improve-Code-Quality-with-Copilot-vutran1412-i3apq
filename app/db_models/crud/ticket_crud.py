from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import Ticket
from typing import List

class TicketCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Ticket)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Ticket]:
        """
        Retrieve all tickets with optional pagination.

        :param skip: Number of records to skip (default is 0).
        :param limit: Maximum number of records to return (default is 10).
        :return: List of Ticket objects.
        """
        result = self.db.execute(
            select(Ticket).offset(skip).limit(limit)
        )
        return result.scalars().all()

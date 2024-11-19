from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.db_models.crud.base_crud import BaseCRUD
from app.db_models.base import Ticket, History
from app.db_models.crud.history_crud import HistoryCRUD
from typing import List, Optional
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicketCRUD(BaseCRUD):
    """
    CRUD operations for Ticket model.

    This class provides methods to perform Create, Read, Update, and Delete (CRUD) operations
    on the Ticket model. It also includes functionality to log changes to ticket status in the history.
    """
    def __init__(self, db: Session):
        """
        Initialize TicketCRUD with a database session.

        :param db: SQLAlchemy Session object.
        """
        super().__init__(db, Ticket)
        self.history_crud = HistoryCRUD(db)

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

    def update_status(self, ticket_id: int, new_status: str, user_id: int) -> Optional[Ticket]:
        """
        Update the status of a ticket and create a history entry.

        :param ticket_id: The ID of the ticket to update.
        :param new_status: The new status of the ticket.
        :param user_id: The ID of the user making the change.
        :return: The updated ticket.
        :raises SQLAlchemyError: If there is an error during the update process.
        """
        try:
            ticket = self.get(ticket_id)
            if not ticket:
                logger.error(f"Ticket with ID {ticket_id} not found")
                raise ValueError("Ticket not found")
            ticket.status = new_status
            self.db.commit()
            self.db.refresh(ticket)

            # Add to history
            self.history_crud.create(
                entity_type="ticket",
                entity_id=ticket_id,
                change_type="status_change",
                user_id=user_id,
                details=f"Status changed to {new_status}"
            )
            logger.info(f"Ticket ID {ticket_id} status updated to {new_status} by user ID {user_id}")
            return ticket
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating ticket ID {ticket_id}: {e}")
            raise e
        except ValueError as ve:
            logger.error(f"Value error: {ve}")
            raise ve

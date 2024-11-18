from sqlalchemy.orm import Session
from app.db_models.crud.ticket_crud import TicketCRUD
import logging

def configure_logger():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logging.basicConfig(level=logging.INFO)
    return logger

logger = configure_logger()

def update_ticket_status(ticket_id: int, new_status: str, user_id: int, db: Session) -> bool:
    """
    Update the status of a ticket.

    Args:
        ticket_id (int): The ID of the ticket.
        new_status (str): The new status of the ticket.
        user_id (int): The ID of the user making the update.
        db (Session): The database session.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        ticket_crud = TicketCRUD(db)
        result = ticket_crud.update_status(ticket_id, new_status, user_id)
        logger.info(f"Ticket {ticket_id} status updated to {new_status} by user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error updating ticket {ticket_id} status: {e}", exc_info=True)
        raise

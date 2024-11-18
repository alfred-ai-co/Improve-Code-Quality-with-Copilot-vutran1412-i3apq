from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db_models.crud.project_crud import ProjectCRUD
import logging

def configure_logger():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logging.basicConfig(level=logging.INFO)
    return logger

logger = configure_logger()

def update_project_status(project_id: int, new_status: str, user_id: int, db: Session) -> bool:
    try:
        project_crud = ProjectCRUD(db)
        result = project_crud.update_status(project_id, new_status, user_id)
        logger.info(f"Project {project_id} status updated to {new_status} by user {user_id}")
        return result
    except SQLAlchemyError as e:  # Use a more specific exception
        logger.error(f"Error updating project {project_id} status: {e}")
        raise

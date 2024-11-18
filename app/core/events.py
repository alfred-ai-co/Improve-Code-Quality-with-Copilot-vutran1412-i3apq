from fastapi import FastAPI
from loguru import logger
from typing import Callable, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os

from app.db_models.base import *
from app.db_models.session import engine, SessionLocal

def create_default_statuses(db: Session, user_id: int = 1) -> None:
    statuses = [
        KanbanStatus(name="Backlog", description="Backlog Status", board_id=1),
        KanbanStatus(name="To Do", description="To Do Status", board_id=1),
        KanbanStatus(name="In Progress", description="In Progress Status", board_id=1),
        KanbanStatus(name="Done", description="Done Status", board_id=1)
    ]
    db.add_all(statuses)
    db.commit()

    # Create default history entries for the statuses
    for status in statuses:
        history_entry = History(
            entity_type="kanban_status",
            entity_id=status.id,
            change_type="create",
            user_id=user_id,  # Dynamic user ID
            details=f"Default Kanban Status '{status.name}' created"
        )
        db.add(history_entry)
    db.commit()

def create_default_board(db: Session) -> None:
    board = KanbanBoard(name="Default Board", description="Default Kanban Board")
    db.add(board)
    db.commit()
    db.refresh(board)

    # Create default history entry for the board
    history_entry = History(
        entity_type="kanban_board",
        entity_id=board.id,
        change_type="create",
        user_id=1,  # Assuming user ID 1 is the admin or system user
        details="Default Kanban Board created"
    )
    db.add(history_entry)
    db.commit()

def create_kanban_defaults(db: Session, create_defaults: Optional[str] = True) -> None:
    logger.debug(f"create_kanban_defaults called with create_defaults={create_defaults}")
    if create_defaults and create_defaults.lower() == 'true':
        logger.info("Creating default Kanban Board and Statuses")
        logger.info("To set off, add env variable CREATE_DEFAULTS=False")
        create_default_board(db)
        create_default_statuses(db)
    elif create_defaults and create_defaults.lower() == 'false':
        logger.info("Create defaults is set to False, not creating default Kanban Board and Statuses")
    else:
        logger.info("No CREATE_DEFAULTS env variable set, not creating default Kanban Board and Statuses")

def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        settings = app.state.settings
        logger.info(f"Starting [{settings.app_env.value}] Application")
        # Start up Events
        load_dotenv(find_dotenv())
        logger.debug("Environment variables loaded")

        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.debug("Database tables created")

        # Create a new session
        session = SessionLocal()
        logger.debug("Database session created")

        # Create default Kanban Board and Statuses
        create_kanban_defaults(session, os.getenv('CREATE_DEFAULTS'))

        # Close session
        session.close()
        logger.debug("Database session closed")

    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        settings = app.state.settings
        logger.info(f"Stopping [{settings.app_env.value}] application")
        # Shut down events
        logger.debug("Application shutdown events completed")
    return stop_app

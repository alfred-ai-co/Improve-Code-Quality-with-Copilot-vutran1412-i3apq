import pytest
import logging
from sqlalchemy.orm import Session
from app.db_models.crud.history_crud import HistoryCRUD
from app.db_models.base import History  # Ensure History model is imported

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def db_session():
    from conftest import override_get_db  # Import the correct override function from conftest
    db = next(override_get_db())
    db.expire_on_commit = False  # Prevent objects from becoming expired on commit
    yield db
    db.close()

@pytest.fixture
def history_crud(db_session: Session):
    return HistoryCRUD(db_session)

def test_create_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_create_history_entry")
    history_entry = history_crud.create(
        entity_type="project",
        entity_id=1,
        change_type="status_change",
        user_id=123,
        details="Status changed to 'In Progress'"
    )
    db_session.commit()  # Commit the session to persist the entry
    logger.info(f"Created history entry: {history_entry}")
    assert history_entry.id is not None
    assert history_entry.details == "Status changed to 'In Progress'"

    # Verify the entry is persisted in the database
    persisted_entry = history_crud.get(history_entry.id)
    logger.info(f"Persisted history entry: {persisted_entry}")
    assert persisted_entry is not None
    assert persisted_entry.details == "Status changed to 'In Progress'"
    logger.info("Finished test_create_history_entry")

def test_get_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_get_history_entry")
    history_entry = history_crud.create(
        entity_type="project",
        entity_id=1,
        change_type="status_change",
        user_id=123,
        details="Status changed to 'In Progress'"
    )
    db_session.commit()  # Commit the session to persist the entry
    fetched_entry = history_crud.get(history_entry.id)
    logger.info(f"Fetched history entry: {fetched_entry}")
    assert fetched_entry is not None
    assert fetched_entry.id == history_entry.id
    logger.info("Finished test_get_history_entry")

def test_get_history_by_entity(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_get_history_by_entity")
    history_crud.create(
        entity_type="project",
        entity_id=1,
        change_type="status_change",
        user_id=123,
        details="Status changed to 'In Progress'"
    )
    db_session.commit()  # Commit the session to persist the entry
    entries = history_crud.get_by_entity_id(entity_type="project", entity_id=1)
    logger.info(f"Fetched history entries: {entries}")
    assert len(entries) > 0
    logger.info("Finished test_get_history_by_entity")

def test_update_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_update_history_entry")
    history_entry = history_crud.create(
        entity_type="project",
        entity_id=1,
        change_type="status_change",
        user_id=123,
        details="Status changed to 'In Progress'"
    )
    db_session.commit()  # Commit the session to persist the entry
    updated_entry = history_crud.update(history_entry.id, details="Status changed to 'Completed'")
    db_session.commit()  # Commit the session to persist the update
    logger.info(f"Updated history entry: {updated_entry}")
    assert updated_entry.details == "Status changed to 'Completed'"

    # Verify the entry is updated in the database
    persisted_entry = history_crud.get(updated_entry.id)
    logger.info(f"Persisted updated history entry: {persisted_entry}")
    assert persisted_entry is not None
    assert persisted_entry.details == "Status changed to 'Completed'"
    logger.info("Finished test_update_history_entry")

def test_delete_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_delete_history_entry")
    history_entry = history_crud.create(
        entity_type="project",
        entity_id=1,
        change_type="status_change",
        user_id=123,
        details="Status changed to 'In Progress'"
    )
    db_session.commit()  # Commit the session to persist the entry
    history_crud.delete(history_entry.id)
    db_session.commit()  # Commit the session to persist the deletion
    logger.info(f"Deleted history entry ID: {history_entry.id}")
    assert history_crud.get(history_entry.id) is None
    logger.info("Finished test_delete_history_entry")

def test_create_history_entry_invalid_data(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_create_history_entry_invalid_data")
    with pytest.raises(ValueError):
        history_crud.create(
            entity_type="project",
            entity_id=None,  # Invalid entity_id
            change_type="status_change",
            user_id=123,
            details="Status changed to 'In Progress'"
        )
    logger.info("Finished test_create_history_entry_invalid_data")

def test_update_nonexistent_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_update_nonexistent_history_entry")
    with pytest.raises(ValueError):
        history_crud.update(
            id=9999,  # Nonexistent ID
            details="Status changed to 'Completed'"
        )
    logger.info("Finished test_update_nonexistent_history_entry")

def test_delete_nonexistent_history_entry(history_crud: HistoryCRUD, db_session: Session):
    logger.info("Starting test_delete_nonexistent_history_entry")
    with pytest.raises(ValueError):
        history_crud.delete(id=9999)  # Nonexistent ID
    logger.info("Finished test_delete_nonexistent_history_entry")

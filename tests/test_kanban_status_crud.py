import pytest
from sqlalchemy.orm import Session
from app.db_models.crud.kanban_status_crud import KanbanStatusCRUD
from app.db_models.base import KanbanStatus

def test_create_kanban_status(db_session: Session):
    kanban_status_crud = KanbanStatusCRUD(db_session)
    kanban_status_data = {"name": "Test Kanban Status", "board_id": 1}
    kanban_status = kanban_status_crud.create(**kanban_status_data)
    assert kanban_status.id is not None
    assert kanban_status.name == "Test Kanban Status"

def test_get_kanban_status(db_session: Session):
    kanban_status_crud = KanbanStatusCRUD(db_session)
    kanban_status_data = {"name": "Test Kanban Status", "board_id": 1}
    kanban_status = kanban_status_crud.create(**kanban_status_data)
    fetched_kanban_status = kanban_status_crud.get(kanban_status.id)
    assert fetched_kanban_status.id == kanban_status.id

def test_update_kanban_status(db_session: Session):
    kanban_status_crud = KanbanStatusCRUD(db_session)
    kanban_status_data = {"name": "Test Kanban Status", "board_id": 1}
    kanban_status = kanban_status_crud.create(**kanban_status_data)
    updated_kanban_status = kanban_status_crud.update(kanban_status.id, name="Updated Kanban Status")
    assert updated_kanban_status.name == "Updated Kanban Status"

def test_delete_kanban_status(db_session: Session):
    kanban_status_crud = KanbanStatusCRUD(db_session)
    kanban_status_data = {"name": "Test Kanban Status", "board_id": 1}
    kanban_status = kanban_status_crud.create(**kanban_status_data)
    kanban_status_crud.delete(kanban_status.id)
    assert kanban_status_crud.get(kanban_status.id) is None

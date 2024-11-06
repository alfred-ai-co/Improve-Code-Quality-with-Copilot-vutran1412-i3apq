import pytest
from sqlalchemy.orm import Session
from app.db_models.crud.kanban_board_crud import KanbanBoardCRUD
from app.db_models.base import KanbanBoard

def test_create_kanban_board(db_session: Session):
    kanban_board_crud = KanbanBoardCRUD(db_session)
    kanban_board_data = {"name": "Test Kanban Board"}
    kanban_board = kanban_board_crud.create(**kanban_board_data)
    assert kanban_board.id is not None
    assert kanban_board.name == "Test Kanban Board"

def test_get_kanban_board(db_session: Session):
    kanban_board_crud = KanbanBoardCRUD(db_session)
    kanban_board_data = {"name": "Test Kanban Board"}
    kanban_board = kanban_board_crud.create(**kanban_board_data)
    fetched_kanban_board = kanban_board_crud.get(kanban_board.id)
    assert fetched_kanban_board.id == kanban_board.id

def test_update_kanban_board(db_session: Session):
    kanban_board_crud = KanbanBoardCRUD(db_session)
    kanban_board_data = {"name": "Test Kanban Board"}
    kanban_board = kanban_board_crud.create(**kanban_board_data)
    updated_kanban_board = kanban_board_crud.update(kanban_board.id, name="Updated Kanban Board")
    assert updated_kanban_board.name == "Updated Kanban Board"

def test_delete_kanban_board(db_session: Session):
    kanban_board_crud = KanbanBoardCRUD(db_session)
    kanban_board_data = {"name": "Test Kanban Board"}
    kanban_board = kanban_board_crud.create(**kanban_board_data)
    kanban_board_crud.delete(kanban_board.id)
    assert kanban_board_crud.get(kanban_board.id) is None

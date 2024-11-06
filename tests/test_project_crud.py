import pytest
from sqlalchemy.orm import Session
from app.db_models.crud.project_crud import ProjectCRUD
from app.db_models.base import Project

def test_create_project(db_session: Session):
    project_crud = ProjectCRUD(db_session)
    project_data = {"name": "Test Project", "description": "Test Description", "kanban_board_id": 1}
    project = project_crud.create(**project_data)
    assert project.id is not None
    assert project.name == "Test Project"

def test_get_project(db_session: Session):
    project_crud = ProjectCRUD(db_session)
    project_data = {"name": "Test Project", "description": "Test Description", "kanban_board_id": 1}
    project = project_crud.create(**project_data)
    fetched_project = project_crud.get(project.id)
    assert fetched_project.id == project.id

def test_update_project(db_session: Session):
    project_crud = ProjectCRUD(db_session)
    project_data = {"name": "Test Project", "description": "Test Description", "kanban_board_id": 1}
    project = project_crud.create(**project_data)
    updated_project = project_crud.update(project.id, name="Updated Project")
    assert updated_project.name == "Updated Project"

def test_delete_project(db_session: Session):
    project_crud = ProjectCRUD(db_session)
    project_data = {"name": "Test Project", "description": "Test Description", "kanban_board_id": 1}
    project = project_crud.create(**project_data)
    project_crud.delete(project.id)
    assert project_crud.get(project.id) is None

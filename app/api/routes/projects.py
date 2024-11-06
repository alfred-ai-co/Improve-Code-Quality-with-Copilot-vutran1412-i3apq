# Project Endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger

from app.db_models.crud import ProjectCRUD
from app.schemas.project import ProjectCreate, ProjectResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Creating project with name: {}", project.name)
    if project.kanban_board_id is None:
        raise HTTPException(status_code=400, detail="kanban_board_id must be provided")
    return project_crud.create(**project.dict())

@router.get("/", status_code=200, response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Fetching all projects")
    return project_crud.get_all()

@router.get("/{id}", status_code=200, response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project = project_crud.get(id)
    if not project:
        logger.error("Project with id {} not found", id)
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
    logger.info("Fetching project with id: {}", id)
    return project

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Updating project with id: {}", id)
    project_crud.update(id, **project.dict())
    return project_crud.get(id)

@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Deleting project with id: {}", id)
    project_crud.delete(id)
    return {"message": "Project deleted successfully"}

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
    try:
        return project_crud.create(**project.dict())
    except Exception as e:
        logger.error("Error creating project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", status_code=200, response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Fetching all projects")
    try:
        return project_crud.get_all()
    except Exception as e:
        logger.error("Error fetching projects: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{id}", status_code=200, response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    try:
        project = project_crud.get(id)
        if not project:
            logger.error("Project with id {} not found", id)
            raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
        logger.info("Fetching project with id: {}", id)
        return project
    except Exception as e:
        logger.error("Error fetching project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Updating project with id: {}", id)
    try:
        project_crud.update(id, **project.dict())
        return project_crud.get(id)
    except Exception as e:
        logger.error("Error updating project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    logger.info("Deleting project with id: {}", id)
    try:
        project_crud.delete(id)
        return {"message": "Project deleted successfully"}
    except Exception as e:
        logger.error("Error deleting project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

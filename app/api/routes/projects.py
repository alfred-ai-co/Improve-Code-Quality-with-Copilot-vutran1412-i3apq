# Project Endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger
from app.db_models.crud.history_crud import HistoryCRUD
from app.db_models.crud import ProjectCRUD
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectWithHistory
from app.api.dependencies.sqldb import get_db
from app.services.project_service import update_project_status

router = APIRouter()

@router.post("/", status_code=201, response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)) -> ProjectResponse:
    """
    Create a new project.
    - **project**: ProjectCreate - The project data to create.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    logger.info("Creating project with name: {}", project.name)
    if project.kanban_board_id is None:
        raise HTTPException(status_code=400, detail="kanban_board_id must be provided")
    try:
        return project_crud.create(**project.model_dump())
    except Exception as e:
        logger.error("Error creating project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", status_code=200, response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)) -> list[ProjectResponse]:
    """
    Get all projects.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    logger.info("Fetching all projects")
    try:
        return project_crud.get_all()
    except Exception as e:
        logger.error("Error fetching projects: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

def _get_project_or_404(project_crud: ProjectCRUD, project_id: int) -> ProjectResponse:
    """
    Helper function to get a project by ID or raise a 404 error.
    - **project_crud**: ProjectCRUD - The project CRUD instance.
    - **project_id**: int - The ID of the project to retrieve.
    """
    project = project_crud.get(project_id)
    if not project:
        logger.error("Project with id {} not found", project_id)
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    return project

@router.get("/{id}", status_code=200, response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db)) -> ProjectResponse:
    """
    Get a project by ID.
    - **id**: int - The ID of the project to retrieve.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    logger.info("Fetching project with id: {}", id)
    try:
        project = _get_project_or_404(project_crud, id)
        return project
    except Exception as e:
        logger.error("Error fetching project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{project_id}/history", response_model=ProjectWithHistory)
def get_project_with_history(project_id: int, db: Session = Depends(get_db)) -> ProjectWithHistory:
    """
    Get a project by ID along with its history.
    - **project_id**: int - The ID of the project to retrieve.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    history_crud = HistoryCRUD(db)
    logger.info("Fetching project with id: {} and its history", project_id)
    try:
        project = _get_project_or_404(project_crud, project_id)
        history = history_crud.get_by_entity_id('project', project_id)
        return {"project": project, "history": history}
    except Exception as e:
        logger.error("Error fetching project with history: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)) -> ProjectResponse:
    """
    Update a project by ID.
    - **id**: int - The ID of the project to update.
    - **project**: ProjectCreate - The project data to update.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    logger.info("Updating project with id: {}", id)
    try:
        project_crud.update(id, **project.model_dump())
        return project_crud.get(id)
    except Exception as e:
        logger.error("Error updating project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{project_id}/status", response_model=ProjectResponse)
def change_project_status(project_id: int, new_status: str, user_id: int, db: Session = Depends(get_db)) -> ProjectResponse:
    """
    Change the status of a project by ID.
    - **project_id**: int - The ID of the project to update.
    - **new_status**: str - The new status of the project.
    - **user_id**: int - The ID of the user making the change.
    - **db**: Session - The database session dependency.
    """
    logger.info("Changing status of project with id: {} to {}", project_id, new_status)
    try:
        project = update_project_status(project_id, new_status, user_id, db)
        return project
    except ValueError as e:
        logger.error("Error changing project status: {}", e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Error changing project status: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a project by ID.
    - **id**: int - The ID of the project to delete.
    - **db**: Session - The database session dependency.
    """
    project_crud = ProjectCRUD(db)
    logger.info("Deleting project with id: {}", id)
    try:
        project_crud.delete(id)
    except Exception as e:
        logger.error("Error deleting project: {}", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

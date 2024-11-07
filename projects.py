import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import create_project, get_project, update_project, delete_project
from .database import get_async_db

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/projects/")
async def create_project_endpoint(project: Project, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await create_project(db, project)
        logger.info(f"Project created: {result}")
        return result
    except ValueError as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}")
async def read_project(project_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await get_project(db, project_id)
        if result:
            logger.info(f"Project retrieved: {result}")
            return result
        else:
            logger.warning(f"Project not found: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
    except RuntimeError as e:
        logger.error(f"Error retrieving project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/projects/{project_id}")
async def update_project_endpoint(project_id: int, project: Project, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await update_project(db, project_id, project)
        logger.info(f"Project updated: {result}")
        return result
    except ValueError as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/projects/{project_id}")
async def delete_project_endpoint(project_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await delete_project(db, project_id)
        if result:
            logger.info(f"Project deleted: {project_id}")
            return {"detail": "Project deleted"}
        else:
            logger.warning(f"Project not found: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
    except RuntimeError as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

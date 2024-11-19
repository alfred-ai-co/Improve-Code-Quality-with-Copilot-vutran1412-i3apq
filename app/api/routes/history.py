from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db_models.crud.history_crud import HistoryCRUD
from app.schemas.history import HistoryCreate, HistoryResponse
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=HistoryResponse, status_code=201)
def create_history_entry(history: HistoryCreate, user_id: int = 1, db: Session = Depends(get_db)) -> HistoryResponse:
    """
    Create a new history entry.
    """
    history_crud = HistoryCRUD(db)
    return history_crud.create(**history.model_dump(), user_id=user_id)

@router.get("/{entity_type}/{entity_id}", response_model=List[HistoryResponse])
def get_history_by_entity(entity_type: str, entity_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[HistoryResponse]:
    """
    Get history entries by entity ID.
    """
    history_crud = HistoryCRUD(db)
    return history_crud.get_by_entity_id(entity_type, entity_id, skip, limit)

@router.put("/{id}", response_model=HistoryResponse)
def update_history_entry(id: int, history: HistoryCreate, db: Session = Depends(get_db)) -> HistoryResponse:
    """
    Update an existing history entry.
    """
    history_crud = HistoryCRUD(db)
    updated_entry = history_crud.update(id, **history.model_dump())
    if not updated_entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return updated_entry

@router.delete("/{id}", response_model=HistoryResponse)
def delete_history_entry(id: int, db: Session = Depends(get_db)) -> HistoryResponse:
    """
    Delete a history entry.
    """
    history_crud = HistoryCRUD(db)
    deleted_entry = history_crud.delete(id)
    if not deleted_entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return deleted_entry

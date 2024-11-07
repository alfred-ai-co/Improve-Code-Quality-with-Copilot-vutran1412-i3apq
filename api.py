import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import add_item, get_item, delete_item
from .database import get_async_db

logger = logging.getLogger(__name__)
app = FastAPI()

@app.post("/items/")
async def create_item(item: Item, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await add_item(db, item)
        logger.info(f"Item created: {result}")
        return result
    except ValueError as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await get_item(db, item_id)
        if result:
            logger.info(f"Item retrieved: {result}")
            return result
        else:
            logger.warning(f"Item not found: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
    except RuntimeError as e:
        logger.error(f"Error retrieving item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item_endpoint(item_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await delete_item(db, item_id)
        if result:
            logger.info(f"Item deleted: {item_id}")
            return {"detail": "Item deleted"}
        else:
            logger.warning(f"Item not found: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
    except RuntimeError as e:
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

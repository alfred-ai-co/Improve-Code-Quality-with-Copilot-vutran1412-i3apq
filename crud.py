import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

async def add_item(db: AsyncSession, item):
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        logger.info(f"Item added: {item}")
        return item
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error: {e.orig}")
        raise ValueError(f"Integrity error: {e.orig}")
    except OperationalError as e:
        await db.rollback()
        logger.error(f"Operational error: {e.orig}")
        raise ConnectionError(f"Operational error: {e.orig}")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e.orig}")
        raise RuntimeError(f"Database error: {e.orig}")

async def get_item(db: AsyncSession, item_id: int):
    try:
        item = await db.get(Item, item_id)
        logger.info(f"Item retrieved: {item}")
        return item
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e.orig}")
        raise RuntimeError(f"Database error: {e.orig}")

async def delete_item(db: AsyncSession, item_id: int):
    try:
        item = await db.get(Item, item_id)
        if item:
            await db.delete(item)
            await db.commit()
            logger.info(f"Item deleted: {item}")
            return True
        logger.warning(f"Item not found: {item_id}")
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e.orig}")
        raise RuntimeError(f"Database error: {e.orig}")

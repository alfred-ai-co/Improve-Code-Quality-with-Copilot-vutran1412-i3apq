import sys
import os
import datetime
import pytz
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_models.base import Base, KanbanBoard

# Add the root directory of the project to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
print("Project root: ", project_root)

# Synchronous fixture for database session
@pytest.fixture(scope='function')
def db_session():
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Add a dummy KanbanBoard to reference in tests
    kanban_board = KanbanBoard(name="Test Board", created_at=datetime.datetime.now(pytz.UTC))
    db.add(kanban_board)
    db.commit()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Asynchronous fixture for async database session
@pytest.fixture(scope='function')
async def async_db_session():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

    engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session and add data within context
    async with async_session() as db:
        kanban_board = KanbanBoard(name="Test Board", created_at=datetime.datetime.now(pytz.UTC))
        db.add(kanban_board)
        await db.commit()

        try:
            yield db  # Provide the session to tests
        finally:
            await db.rollback()  # Rollback in case of modifications in the test

    # Drop tables after all tests complete
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

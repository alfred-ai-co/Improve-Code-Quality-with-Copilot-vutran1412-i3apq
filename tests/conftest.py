import sys
import os
import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db_models.base import Base, KanbanBoard
from app.api.dependencies import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    logger.info("Creating TestClient fixture")
    with TestClient(app) as c:
        yield c
    logger.info("TestClient fixture closed")

# Ensure the database schema is reset before each test
@pytest.fixture(scope='function', autouse=True)
def reset_database():
    logger.info("Resetting database schema")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema reset")

# Create a new database session for each test
@pytest.fixture(scope='function')
def db_session():
    logger.info("Creating new database session for test")
    db = TestingSessionLocal()
    # Add a dummy KanbanBoard to reference in tests
    try:
        kanban_board = KanbanBoard(name="Test Board")
        db.add(kanban_board)
        db.commit()
        logger.info("Added dummy KanbanBoard to database")
    except Exception as e:
        logger.error(f"Error adding dummy KanbanBoard: {e}")
        db.rollback()
    try:
        yield db
    finally:
        db.close()
        logger.info("Database session closed")

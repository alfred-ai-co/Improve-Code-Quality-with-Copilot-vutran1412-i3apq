from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import datetime


Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    kanban_board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)

    kanban_board = relationship("KanbanBoard", back_populates="projects")
    tickets = relationship("Ticket", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    kanban_status_id = Column(Integer, ForeignKey("kanban_statuses.id"), nullable=False)

    project = relationship("Project", back_populates="tickets")
    kanban_status = relationship('KanbanStatus', back_populates='tickets')

    def __repr__(self):
        return f"<Ticket(id={self.id}, title={self.title}, status={self.status})>"

class KanbanBoard(Base):
    """
    Represents a Kanban board which contains multiple projects and statuses.
    """
    __tablename__ = "kanban_boards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    projects = relationship('Project', back_populates='kanban_board')
    statuses = relationship('KanbanStatus', back_populates='kanban_board')

    def __repr__(self):
        return f"<KanbanBoard(id={self.id}, name={self.name})>"

class KanbanStatus(Base):
    """
    Represents a status within a Kanban board, such as 'To Do', 'In Progress', or 'Done'.
    """
    __tablename__ = "kanban_statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    kanban_board = relationship('KanbanBoard', back_populates='statuses')
    tickets = relationship('Ticket', back_populates='kanban_status')

    def __repr__(self):
        return f"<KanbanStatus(id={self.id}, name={self.name})>"

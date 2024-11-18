import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, foreign

Base = declarative_base()
metadata = MetaData()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    kanban_board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    kanban_status_id = Column(Integer, ForeignKey("kanban_statuses.id"), nullable=False)

    def __repr__(self):
        return f"<Ticket(id={self.id}, title={self.title}, status={self.status})>"

class KanbanBoard(Base):
    __tablename__ = "kanban_boards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<KanbanBoard(id={self.id}, name={self.name})>"

class KanbanStatus(Base):
    __tablename__ = "kanban_statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<KanbanStatus(id={self.id}, name={self.name})>"

class History(Base):
    __tablename__ = "history"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_type = Column(String(50), nullable=False)  # "Project" or "Ticket"
    entity_id = Column(Integer, nullable=False)  # References the ID of the associated project or ticket
    change_type = Column(String(50), nullable=False)  # Type of change (e.g., "status_change", "comment")
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False)  # When the change was made
    user_id = Column(Integer, nullable=False)  # References the ID of the user who made the change
    details = Column(Text, nullable=True)  # Detailed description of the change

    def __repr__(self):
        return f"<History(id={self.id}, entity_type={self.entity_type}, entity_id={self.entity_id}, change_type={self.change_type})>"

def add_relationships():
    Project.tickets = relationship("Ticket", back_populates="project")
    Project.kanban_board = relationship("KanbanBoard", back_populates="projects")
    Project.history = relationship("History", back_populates="project", primaryjoin="and_(Project.id==foreign(History.entity_id), History.entity_type=='project')", overlaps="ticket")

    Ticket.project = relationship("Project", back_populates="tickets")
    Ticket.kanban_status = relationship('KanbanStatus', back_populates='tickets')
    Ticket.history = relationship("History", back_populates="ticket", primaryjoin="and_(Ticket.id==foreign(History.entity_id), History.entity_type=='ticket')", overlaps="project")

    KanbanBoard.projects = relationship('Project', back_populates='kanban_board')
    KanbanBoard.statuses = relationship('KanbanStatus', back_populates='kanban_board')

    KanbanStatus.kanban_board = relationship('KanbanBoard', back_populates='statuses')
    KanbanStatus.tickets = relationship('Ticket', back_populates='kanban_status')

    History.project = relationship("Project", back_populates="history", primaryjoin="and_(foreign(History.entity_id)==Project.id, History.entity_type=='project')", viewonly=True)
    History.ticket = relationship("Ticket", back_populates="history", primaryjoin="and_(foreign(History.entity_id)==Ticket.id, History.entity_type=='ticket')", viewonly=True)

add_relationships()

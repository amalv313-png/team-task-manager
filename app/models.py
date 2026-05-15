import enum
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.MEMBER)

    tasks: Mapped[List["Task"]] = relationship(back_populates="assignee")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Cascading Deletes: when a project is deleted, orphan tasks are deleted
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    project: Mapped["Project"] = relationship(back_populates="tasks")
    assignee: Mapped[Optional["User"]] = relationship(back_populates="tasks")

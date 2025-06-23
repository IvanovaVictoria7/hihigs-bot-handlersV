__all__ = [
    "User",
    "Base",
    "Profile",
    "Task"
]

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey, String
from typing import Optional, List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, default="Unknown")
    tutorcode: Mapped[Optional[str]] = mapped_column(VARCHAR(6), nullable=True)
    subscribe: Mapped[Optional[str]] = mapped_column(VARCHAR(6), nullable=True)
    extra: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    profiles: Mapped[List["Profile"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Profile(Base):
    tablename = "profile_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.user_id"))
    profile_url: Mapped[str] = mapped_column(String(255))

    owner: Mapped["User"] = relationship(back_populates="profiles")
    tasks: Mapped[List["Task"]] = relationship(back_populates="profile", cascade="all, delete-orphan")


class Task(Base):
    tablename = "task_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile_table.id"))
    task_name: Mapped[str] = mapped_column(String(255))

    profile: Mapped["Profile"] = relationship(back_populates="tasks")


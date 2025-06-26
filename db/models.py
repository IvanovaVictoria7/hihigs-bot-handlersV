__all__ = [
    "User",
    "Base",
    "Profile",
    "Task",
    "Subscription"
]

from sqlalchemy import Column, Integer, Text, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True)
    user_name = Column(VARCHAR(255),nullable=False, default="Unknown")
    role = Column(VARCHAR(20),nullable=False, default="student")  # student или teacher
    extra = Column(Text,nullable=True)
    tutorcode = Column(VARCHAR(100), nullable=True)


    profiles = relationship("Profile",      back_populates="owner")
    students = relationship("Subscription", back_populates="teacher", foreign_keys="[Subscription.teacher_id]")
    teachers = relationship("Subscription", back_populates="student", foreign_keys="[Subscription.student_id]")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    profile_url = Column(VARCHAR(255), nullable=False)

    owner = relationship("User",back_populates="profiles")
    tasks = relationship("Task", back_populates="profile")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    task_name = Column(VARCHAR(255), nullable=False)

    profile = relationship("Profile", back_populates="tasks")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.user_id"))
    student_id = Column(Integer, ForeignKey("users.user_id"))

    teacher = relationship("User", back_populates="students", foreign_keys=[teacher_id])
    student = relationship("User", back_populates="teachers", foreign_keys=[student_id])
"""Plane model to handle objects."""

from pydantic import BaseModel, PastDatetime, EmailStr


class Project(BaseModel):
    """Plane project model to handle project object."""

    id: str
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime


class User(BaseModel):
    """Plane user model to handle user object."""

    id: int
    name: str
    email: EmailStr
    created_at: PastDatetime
    updated_at: PastDatetime


class Task(BaseModel):
    """Plane task model to handle task object."""

    id: int
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime

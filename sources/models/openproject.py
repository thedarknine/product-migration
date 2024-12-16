"""OpenProject project model to handle project object."""

from pydantic import BaseModel, PastDatetime, EmailStr


class Project(BaseModel):
    """OpenProject project model to handle project object."""

    id: int
    name: str
    identifier: str
    createdAt: PastDatetime
    updatedAt: PastDatetime


class User(BaseModel):
    """OpenProject user model to handle user object."""

    id: int
    name: str
    email: EmailStr
    createdAt: PastDatetime
    updatedAt: PastDatetime

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class Task(BaseModel):
    """OpenProject task model to handle task object."""

    id: int
    name: str
    createdAt: PastDatetime
    updatedAt: PastDatetime

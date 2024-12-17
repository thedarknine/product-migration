"""OpenProject project model to handle project object."""

from pydantic import BaseModel, PastDatetime, EmailStr


class Project(BaseModel):
    """OpenProject project model to handle project object."""

    id: int
    name: str
    identifier: str
    createdAt: PastDatetime
    updatedAt: PastDatetime

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


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


class State(BaseModel):
    """OpenProject state model to handle state object."""

    id: int
    name: str

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class Type(BaseModel):
    """OpenProject type model to handle type object."""

    id: int
    name: str
    color: str | None = None

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class Task(BaseModel):
    """OpenProject task model to handle task object."""

    id: int
    subject: str
    createdAt: PastDatetime
    updatedAt: PastDatetime

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()

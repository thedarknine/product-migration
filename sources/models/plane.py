"""Plane model to handle objects."""

from pydantic import BaseModel, PastDatetime, EmailStr


class Project(BaseModel):
    """Plane project model to handle project object."""

    id: str
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class User(BaseModel):
    """Plane user model to handle user object."""

    id: str
    first_name: str
    last_name: str
    email: EmailStr

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class State(BaseModel):
    """Plane state model to handle state object."""

    id: str
    name: str
    group: str | None = None

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()


class Task(BaseModel):
    """Plane task model to handle task object."""

    id: str
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime

    def __hash__(self) -> int:
        """Hash function.

        Returns:
            int: Hash value.
        """
        return self.id.__hash__()

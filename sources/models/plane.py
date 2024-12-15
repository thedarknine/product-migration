"""Plane model to handle objects."""

from pydantic import BaseModel, PastDatetime


class Project(BaseModel):
    """Plane project model to handle project object."""

    id: str
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime

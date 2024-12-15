"""OpenProject project model to handle project object."""

from pydantic import BaseModel, PastDatetime


class Project(BaseModel):
    """OpenProject project model to handle project object."""

    id: int
    name: str
    identifier: str
    createdAt: PastDatetime
    updatedAt: PastDatetime

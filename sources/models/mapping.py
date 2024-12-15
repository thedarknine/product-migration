"""Mapping model."""

from pydantic import BaseModel


class OpenProject(BaseModel):
    """OpenProject model into mapping configuration."""

    exclude_projects: list | None


class Plane(BaseModel):
    """Plane model into mapping configuration."""

    exclude_users: list | None


class Mapping(BaseModel):
    """Mapping model into mapping configuration."""

    openproject: OpenProject
    plane: Plane

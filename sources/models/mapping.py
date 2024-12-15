from pydantic import BaseModel


class OpenProject(BaseModel):
    exclude_projects: list | None

class Plane(BaseModel):
    exclude_users: list | None

class Mapping(BaseModel):
    openproject: OpenProject
    plane: Plane
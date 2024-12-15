from pydantic import BaseModel, PastDatetime


class Project(BaseModel):
    id: int
    name: str
    identifier: str
    createdAt: PastDatetime
    updatedAt: PastDatetime

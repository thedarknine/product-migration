from pydantic import BaseModel, PastDatetime


class Project(BaseModel):
    id: str
    name: str
    created_at: PastDatetime
    updated_at: PastDatetime

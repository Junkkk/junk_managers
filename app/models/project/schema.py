from pydantic import BaseModel


class Project(BaseModel):
    name: str
    company_id: int

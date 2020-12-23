from pydantic import BaseModel
from .db_model import GlobalRoleEnum


class User(BaseModel):
    name: str
    role: GlobalRoleEnum
    company_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from .db_model import ProjectRoleEnum


class Membership(BaseModel):
    user_id: int
    project_id: int
    role: ProjectRoleEnum

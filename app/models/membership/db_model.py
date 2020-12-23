import enum

from sqlalchemy import Column, Integer, Enum, ForeignKey
from app.db.session import Base


class ProjectRoleEnum(str, enum.Enum):
    admin = 'Администратор'
    manager = 'Менеджер'


class Membership(Base):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(Enum(ProjectRoleEnum))

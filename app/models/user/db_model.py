import enum

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from app.db.session import Base


class GlobalRoleEnum(str, enum.Enum):
    owner = 'Владелец'
    employee = 'Сотрудник'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    role = Column(Enum(GlobalRoleEnum))
    company_id = Column(Integer, ForeignKey("companies.id"))


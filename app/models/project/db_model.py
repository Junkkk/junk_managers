from sqlalchemy import Column, String, Integer, ForeignKey
from app.db.session import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    company_id = Column(Integer, ForeignKey("companies.id"))

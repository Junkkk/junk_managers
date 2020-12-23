from sqlalchemy import Column, String, Integer
from app.db.session import Base


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # def __dict__(self):
    #     return f'id: {self.id}, name: {self.name}'
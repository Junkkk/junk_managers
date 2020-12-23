from pydantic import BaseModel


class Company(BaseModel):
    name: str


class CompanyDB(Company):
    id: int

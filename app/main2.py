import enum

from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("postgresql://postgres:postgres@localhost/managers")
Session = sessionmaker(bind=engine)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class GlobalRoleEnum(str, enum.Enum):
    owner = 'Владелец'
    employee = 'Сотрудник'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    role = Column(Enum(GlobalRoleEnum))
    company_id = Column(Integer, ForeignKey("companies.id"))


class ProjectRoleEnum(str, enum.Enum):
    admin = 'Администратор'
    manager = 'Менеджер'


class Membership(Base):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(Enum(ProjectRoleEnum))


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    company_id = Column(Integer, ForeignKey("companies.id"))


if __name__ == '__main__':
    session = Session()
    user_id = 2
    t = session.execute(
        f"""
        select users."name" as "username"
	          ,projects."name" as "project_name"
        from users 
		   left join memberships on users.id = memberships.user_id 
		   left join projects on memberships.project_id = projects.id
		   left join companies on companies.id = users.company_id and companies.id = projects.company_id 
        where users."role" = 'employee' 
        and companies.name = (select companies."name" 
                              from companies where id = (select company_id from users where users.id = {user_id}))
        and 'owner' = (select users."role" from users where id = {user_id})
        union all 
        select users."name" as "username"
	          ,projects."name" as "project_name"
        from users 
		   left join memberships on users.id = memberships.user_id 
		   left join projects on memberships.project_id = projects.id
        where users."role" = 'employee'
        and memberships."role" = 'manager'
        and projects.id in (select memberships.project_id 
                            from users left join memberships on users.id = memberships.user_id 
                            where users.id = {user_id} and memberships.role = 'admin')
        union all 
        select users.name as "username"
	          ,projects.name as "project_name"
        from users 
		   left join memberships on users.id = memberships.user_id 
		   left join projects on memberships.project_id = projects.id
        where users.role = 'employee'
        and memberships.role = 'manager'
        and users.id = {user_id}
        """)
    for i in t:
        print(i)
    print(session.query(User).filter(User.name == 'Anton').first().id)
    session.close()

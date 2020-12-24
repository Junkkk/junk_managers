from sqlalchemy.orm import Session


async def manager_list(db: Session, user_id: int):
    from_db = db.execute(f"""
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
    out_data = {}
    for name, project in from_db:
        if project not in out_data:
            out_data[project] = []
        out_data[project].append(name)
    return out_data

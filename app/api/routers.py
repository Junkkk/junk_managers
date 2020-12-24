from fastapi import APIRouter
from app.api.endpoints import companies, memberships, projects, users, managers, login


router = APIRouter()
router.include_router(companies.router)
router.include_router(users.router)
router.include_router(projects.router)
router.include_router(memberships.router)
router.include_router(managers.router)
router.include_router(login.router)

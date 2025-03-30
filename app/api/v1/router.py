from fastapi import APIRouter

from app.api.v1 import commands, endpoints

# Create the main API router
router = APIRouter(prefix="/v1")
router.include_router(commands.router)
router.include_router(endpoints.router)

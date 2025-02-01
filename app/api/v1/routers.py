from fastapi import APIRouter, Depends

from app.utils.middlewares.headers import set_v1_bknd_common_header
from app.api.v1 import commands, endpoints

# Create the main API router
router = APIRouter(prefix="/v1")
router.include_router(commands.router, dependencies=[Depends(set_v1_bknd_common_header)])
router.include_router(endpoints.router, dependencies=[Depends(set_v1_bknd_common_header)])

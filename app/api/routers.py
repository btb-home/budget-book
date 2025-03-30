from fastapi import APIRouter

from app.api.v1.router import router as v1_router
from app.schemas.systems import responses

routers = APIRouter(prefix="/api")
routers.include_router(router=v1_router)

routers.responses[400] = {"model": responses.JSendFailure}
routers.responses[500] = {"model": responses.JSendError}

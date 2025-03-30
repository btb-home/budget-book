from fastapi import APIRouter

from app.schemas.systems import responses

from app.api.v1.router import router as v1_router

routers = APIRouter(prefix="/api")
routers.include_router(router=v1_router)

routers.responses[400] = {"model": responses.FailureResponse}
routers.responses[500] = {"model": responses.ErrorResponse}

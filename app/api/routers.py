from fastapi import APIRouter

from app.schemas.systems import responses

from app.api.v1.routers import router as v1_router

api_router = APIRouter(prefix="/api")
api_router.include_router(router=v1_router)

api_router.responses[400] = {"model": responses.FailureResponse}
api_router.responses[500] = {"model": responses.ErrorResponse}

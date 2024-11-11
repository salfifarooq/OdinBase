from __future__ import annotations

import logging

from fastapi import APIRouter, status

from app.model.response import Response
from app.routes.api_db import router as item_service_router
from app.routes.api_grpc import router as api_grpc_router
from app.routes.api_router import router as api_router

logger = logging.getLogger("custom")

router = APIRouter(
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Response}
    },  # additional status code and their corresponding response model
)


@router.get("/")
async def index() -> dict[str, str]:
    return {
        "info": "This is the index page of this template "
        "You probably want to go to 'http://<hostname:port>/docs'.",
    }


router.include_router(api_router, prefix="/api_router", tags=["api_router"])
router.include_router(
    api_grpc_router,
    prefix="/api_grpc",
    tags=["api_grpc"],
)
router.include_router(
    item_service_router,
    prefix="/items",
    tags=["api_items"],
)

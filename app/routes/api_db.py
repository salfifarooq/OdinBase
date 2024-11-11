from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Response, status

from app.apis.api_items.model.items import ItemCreate
from app.apis.api_items.srv.main import ItemService
from app.core.auth import get_current_user
from app.model.response import Response as HTTPResponse

router = APIRouter()
# Uses the JSON logger
logger = logging.getLogger("json")

item_service_instance = ItemService()

# Initialize the router and add item_service as a dependency
router = APIRouter(
    dependencies=[Depends(get_current_user), Depends(lambda: item_service_instance)]
)


@router.get("/", response_model=HTTPResponse, status_code=status.HTTP_200_OK)
async def get_all_items(
    response: Response,
    item_service: ItemService = Depends(lambda: item_service_instance),
) -> HTTPResponse:
    """
    Retrieve all the items from the items table.
    """
    try:
        result = await item_service.get_all_items()
        return HTTPResponse(data=result)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"error retrieving data {e}")
        return HTTPResponse(error=str(e))


@router.post("/", response_model=HTTPResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    response: Response,
    item_service: ItemService = Depends(lambda: item_service_instance),
) -> HTTPResponse:
    """
    Create item.
    """
    try:
        result = await item_service.create_item(data=data)
        return HTTPResponse(data=result)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"error retrieving data {e}")
        return HTTPResponse(error=str(e))

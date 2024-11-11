from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Response, status

from app.apis.api_b_grpc.srv.main import BakerService
from app.core.auth import get_current_user
from app.dependencies.grpc_service.model.response import OrderRequest
from app.model.response import Response as HTTPResponse

# Initialize router and logger
router = APIRouter()
logger = logging.getLogger("custom")

# Create the BakerService instance to use across the router
baker_service_instance = BakerService()

# Initialize the router and add baker_service as a dependency
router = APIRouter(
    dependencies=[Depends(get_current_user), Depends(lambda: baker_service_instance)]
)


@router.get("/{num}", response_model=HTTPResponse, status_code=status.HTTP_200_OK)
async def get_order_status(
    num: int,
    response: Response,
    current_user: Depends = Depends(get_current_user),
    baker_service: BakerService = Depends(lambda: baker_service_instance),
) -> HTTPResponse:
    """
    Retrieves an order based on the given order number.

    - `num`: The order ID number.
    - `response`: FastAPI Response object for custom status handling.
    - `current_user`: The currently authenticated user.
    - `baker_service`: Dependency-injected BakerService instance.
    """
    logger.info(f"fetching order with num={num} for user={current_user.username}")

    result = baker_service.do(input=OrderRequest(num=num))

    if not result.success:
        logger.error(f"failed to retrieve order: {result.error}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPResponse(error=result.error)
    # above: can prefer not to give the exact error
    # todo: error handling as per logic

    if not result.data:
        logger.warning(f"no data found for order num={num}")
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPResponse(error="Order not found")

    logger.info(f"retrieved order data for num={num}")
    return HTTPResponse(data=result.data)

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Response, status

from app.apis.api_router.srv.expensive import ExpensiveTaskService
from app.apis.api_router.srv.main import main_func as main_func_a
from app.core.auth import get_current_user
from app.model.response import Response as HTTPResponse

router = APIRouter()
# Uses the JSON logger
logger = logging.getLogger("json")

tasks = ExpensiveTaskService()


@router.get("/{num}", response_model=HTTPResponse, status_code=status.HTTP_200_OK)
async def view_a(
    num: int,
    response: Response,
    _: Depends = Depends(get_current_user),
) -> HTTPResponse:
    """
    Retrieve random data associated with the given number.

    - **num**: Seed identifier for the data to retrieve.
    """
    logger.info(f"Fetching data for num={num}")

    try:
        result = main_func_a(num)
        logger.info(f"retrieved data for num={num}: {result}")
        return HTTPResponse(data=result)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"error retrieving data for num={num}: {e}")
        return HTTPResponse(error=str(e))


@router.get("/compute/", response_model=HTTPResponse, status_code=status.HTTP_200_OK)
async def expensive_compute(
    x: int,
    y: int,
    response: Response,
    _: Depends = Depends(get_current_user),
) -> HTTPResponse:
    """
    Simulate an expensive calculation.

    - **x**: value 1
    - **y**: value 2
    """
    logger.info(f"computing x = {x} and y = {y}")

    try:
        task_id = tasks.submit_add_task(x, y)
        logger.info(f"task id: {task_id}")
        return HTTPResponse(data=task_id)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"error computing x = {x} and y = {y}: {e}")
        return HTTPResponse(error=str(e))


@router.get(
    "/compute/status", response_model=HTTPResponse, status_code=status.HTTP_200_OK
)
async def expensive_compute_status(
    task_id: str,
    response: Response,
    _: Depends = Depends(get_current_user),
) -> HTTPResponse:
    """
    Gets the status of the computed task.

    - **task_id**: the task id of celery
    """
    logger.info(f"task id received: {task_id}")

    try:
        response = tasks.get_task_status(task_id=task_id)
        return HTTPResponse(data=response)

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"error retrieving for task_id {task_id}: {e}")
        return HTTPResponse(error=f"{str(e)}")

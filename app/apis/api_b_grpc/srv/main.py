from __future__ import annotations

import logging
import re
from typing import Dict

from circuitbreaker import CircuitBreakerError

from app.dependencies.grpc_service.model.response import (OrderRequest,
                                                          OrderResponse)
from app.dependencies.grpc_service.srv import bakery_service

logger = logging.getLogger("json")
# mock: num: int to order: str
dessert_map: Dict[int, str] = {1: "cookie", 2: "donut", 3: "gelato"}


class BakerService:
    """Service for interacting with the Bakery gRPC client."""

    def __init__(self) -> None:
        """Initialize the BakerService with a gRPC client."""
        self.grpc_client = bakery_service.BakeryClient()

    def do(self, input: OrderRequest) -> OrderResponse:
        """Process an order request.

        Args:
            input (OrderRequest): The order request containing details.

        Returns:
            OrderResponse: The response containing order data or error information.
        """
        try:
            logger.info(
                f"processing order for dessert: {dessert_map.get(input.num)} (order_id: {input.num})"
            )

            result = self.grpc_client.get_order(order=dessert_map.get(input.num))
            logger.info(f"successfully processed order: {result}")
            return result

        except CircuitBreakerError as e:
            logger.error(f"circuit active {input.num}: {e}")
            match = re.search(r"(\d+ failures, \d+ sec remaining)", str(e))
            failure_info = match.group(1) if match else "Unknown failure info"

            logger.error(f"circuit open: {failure_info}")
            return OrderResponse(
                success=False,
                error=f"circuit open: {failure_info}",
            )
        except Exception as e:
            logger.error(f"error processing order {input.num}: {e}")
            return OrderResponse(success=False, error=str(e))

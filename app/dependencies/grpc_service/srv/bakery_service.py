import logging

import circuitbreaker
import grpc
from google.protobuf.json_format import MessageToDict

from app.core import config
from app.dependencies.grpc_service.model.response import OrderResponse
from bakery_grpc.pb.bakery_pb2 import OrderRequest
from bakery_grpc.pb.bakery_pb2_grpc import BakeryStub

logger = logging.getLogger("custom")


class BakeryClient:
    """Client for interacting with the Bakery gRPC service."""

    def __init__(self) -> None:
        """Initialize the gRPC channel and stub."""
        self.channel = grpc.insecure_channel(config.BAKERY_SERVICE)
        self.stub = BakeryStub(self.channel)

    @circuitbreaker.circuit(recovery_timeout=10, failure_threshold=5)
    def get_order(self, order: str | None) -> OrderResponse:
        """Get an order from the Bakery service.

        Args:
            order (str): The name of the order to request.

        Returns:
            OrderResponse: The response containing order data or error information.
        """
        try:
            # Call the gRPC service to get the order
            grpc_response = self.stub.GetOrder(OrderRequest(order=order))
            return OrderResponse(
                success=True,
                data=MessageToDict(grpc_response, preserving_proto_field_name=True),
            )

        except grpc.RpcError as rpc_error:
            logger.error(f"error occurred: {rpc_error.code()} - {rpc_error.details()}")
            raise grpc.RpcError(rpc_error.details())

    def close(self) -> None:
        """Close the gRPC channel."""
        self.channel.close()

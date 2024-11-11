from grpc import StatusCode
from grpc_interceptor.exceptions import GrpcException, NotFound
from pb.bakery_pb2 import OrderRequest, OrderResponse
from pb.bakery_pb2_grpc import BakeryServicer

mock_desserts = {"cookie": 10, "donut": 5, "gelato": 0}


class BakeryBaseService(BakeryServicer):
    def GetOrder(self, request: OrderRequest, context) -> OrderResponse:
        desserts_stock = mock_desserts.get(request.order)

        if desserts_stock is None:
            raise GrpcException(
                details="Dessert not found",
                status_code=StatusCode.NOT_FOUND,
            )

        if desserts_stock == 0:
            raise NotFound(details="Dessert out of stock")

        return OrderResponse(order_status="Delivery!")

import logging
from concurrent import futures

import grpc
from core.config import settings
from grpc_interceptor import ExceptionToStatusInterceptor
from pb.bakery_pb2_grpc import add_BakeryServicer_to_server
from services.bakery import BakeryBaseService


class BakeryService(BakeryBaseService):
    pass


def serve() -> None:
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_BakeryServicer_to_server(BakeryService(), server)
    server.add_insecure_port(f"[::]:{settings.SERVICE_PORT}")

    server.start()
    try:
        logging.info(f"bakery service starting on {settings.SERVICE_PORT}")
        logging.info("bakery server is running and awaiting requests.")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("keyboard interrupt received. Shutting down bakery server.")
    except Exception as e:
        logging.error(f"unexpected error occurred: {e}")
    finally:
        server.stop(grace=5)
        logging.info("bakery server has been stopped gracefully.")


if __name__ == "__main__":
    logging.basicConfig(level=settings.logging_level, format=settings.log_format)
    serve()

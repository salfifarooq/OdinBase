import logging

from pythonjsonlogger import jsonlogger


def configure_logger() -> None:
    """Configure a custom logger."""

    # Create a logger
    logger = logging.getLogger("custom")
    logger.setLevel(logging.INFO)

    # Create a handler (console output in this case)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    # Disable propagation to avoid log duplication via uvicorn
    logger.propagate = False

    # Disable passlib logger
    # See: <https://github.com/pyca/bcrypt/issues/684>
    logging.getLogger("passlib").setLevel(logging.ERROR)


def configure_json_logger() -> None:
    """Configure a custom json logger."""
    logger = logging.getLogger("json")
    logger.setLevel(logging.DEBUG)  # todo: from config

    stream_handler = logging.StreamHandler()

    # Set up JSON formatter with desired format
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d"
    )

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a handler (console output in this case)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    # Disable propagation to avoid log duplication via uvicorn
    logger.propagate = False

    # Disable passlib logger
    # See: <https://github.com/pyca/bcrypt/issues/684>
    logging.getLogger("passlib").setLevel(logging.ERROR)

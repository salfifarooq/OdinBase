import logging
import os
import pathlib

from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")


class GlobalConfig:
    title: str = os.getenv("TITLE", "")
    version: str = "1.0.0"
    description: str = os.getenv("DESCRIPTION", "")
    log_format: str = os.getenv("LOG_FORMAT", "")
    logging_level: int = logging.DEBUG
    SERVICE_PORT: str = os.getenv("SERVICE_PORT", "")


settings = GlobalConfig()

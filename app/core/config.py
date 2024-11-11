import pathlib

from starlette.config import Config

ROOT = pathlib.Path(__file__).resolve().parent.parent  # app/
BASE_DIR = ROOT.parent  # ./

config = Config(BASE_DIR / ".env")

API_USERNAME = config("API_USERNAME", str)
API_PASSWORD = config("API_PASSWORD", str)

# Auth configs.
API_SECRET_KEY = config("API_SECRET_KEY", str)
API_ALGORITHM = config("API_ALGORITHM", str)

API_ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "API_ACCESS_TOKEN_EXPIRE_MINUTES", int
)  # infinity

BAKERY_SERVICE: str = config("BAKERY_SERVICE", str)

# postgres
POSTGRES_USER: str = config("POSTGRES_USER", str)
POSTGRES_PASS: str = config("POSTGRES_PASS", str)
POSTGRES_HOST: str = config("POSTGRES_HOST", str)
POSTGRES_DB_NAME: str = config("POSTGRES_DB_NAME", str)

# celery
CELERY_BROKER: str = config("CELERY_BROKER", str)
CELERY_BACKEND: str | None = config("CELERY_BACKEND", default=None)

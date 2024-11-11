from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def api_token() -> str:
    # Get token.
    res = client.post(
        "/token",
        headers={"Accept": "application/x-www-form-urlencoded"},
        data={
            "username": config.API_USERNAME,
            "password": config.API_PASSWORD,
        },
    )
    res_json = res.json()

    access_token = res_json["access_token"]
    token_type = res_json["token_type"]

    return f"{token_type} {access_token}"


def test_api_a_unauthorized() -> None:
    """Should return 401."""

    # Unauthorized request.
    response = client.get("/api_router/100")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_api_a_invalid_input(api_token):
    """Should return 422."""

    # Authorized but should raise 400 error.
    response = client.get(
        "/api_router/a",
        headers={
            "Accept": "application/json",
            "Authorization": api_token,
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_api_a_ok(api_token):
    # Successful request.
    response = client.get(
        "/api_router/200",
        headers={
            "Accept": "application/json",
            "Authorization": api_token,
        },
    )
    assert response.status_code == HTTPStatus.OK

    data = (
        response.json()
    )  # Assuming response.json() returns the nested dictionary structure

    for val in data.values():
        if val is None:
            continue
        if isinstance(val, dict):
            for v in val.values():
                assert isinstance(v, int)
        else:
            assert isinstance(val, int)

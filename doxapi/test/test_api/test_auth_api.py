import jwt
import pytest

from doxapi.app import app

AUTH_URL = "/auth"

SECRET_KEY = app.config["SECRET_KEY"]
JWT_ALGORITHM = app.config["JWT_ALGORITHM"]


def test_api_returns_access_token_and_user_data(api_client, user):
    credentials = {"email": user.email, "password": user.password}
    resp = api_client.post(AUTH_URL, credentials)
    assert resp.status_code == 200
    assert resp.json["user"]["id"] == user.id
    assert resp.json["user"]["name"] == user.name
    assert resp.json["user"]["email"] == user.email

    token = jwt.decode(
        resp.json["access_token"], SECRET_KEY, algorithms=[JWT_ALGORITHM]
    )
    assert token["identity"] == user.id


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"email": "invalid@exmaple.com"},
        {"email": "invalid@exmaple.com", "password": "invalid"},
        {"password": "invalid"},
    ],
)
def test_api_returns_401_on_invalid_credentials(api_client, user, invalid_data):
    invalid_credentials = {
        "email": invalid_data.get("email", user.email),
        "password": invalid_data.get("password", user.password),
    }
    resp = api_client.post(AUTH_URL, invalid_credentials)
    assert resp.status_code == 401


def test_api_returs_401_on_missing_auth_token(api_client):
    resp = api_client.get(AUTH_URL, headers={})
    assert resp.status_code == 401


def test_api_returs_422_on_invalid_auth_token(api_client):
    resp = api_client.get(AUTH_URL, headers={"Authorization": "invalid"})
    assert resp.status_code == 422


def test_api_returns_user_data(auth_client, user):
    resp = auth_client.get(AUTH_URL)
    assert resp.status_code == 200
    assert resp.json["id"] == user.id
    assert resp.json["name"] == user.name
    assert resp.json["email"] == user.email

from http import HTTPStatus
from typing import Any

import requests
from django.conf import settings


class SSOServerError(Exception):
    pass


def get_jwt(authorization_code: str, redirect_uri: str) -> dict[str, Any]:
    """Exchange authorization code for JWT tokens.

    Args:
        authorization_code (str): authorization code from SSO
        redirect_uri (str): redirect uri after authorization

    Raises:
        SSOServerError: If SSO server returns an error

    Returns:
        dict[str, Any]: payload with JWT tokens
    """
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": settings.SSO_CLIENT_ID,
        "client_secret": settings.SSO_CLIENT_SECRET,
    }
    response = requests.post(
        settings.SSO_TOKEN_URL,
        data=payload,
        timeout=20,
    )
    if response.status_code != HTTPStatus.OK:
        error_msg = "Unknown error"
        try:
            error_data = response.json()
            if "error_description" in error_data:
                error_msg = error_data["error_description"]
            elif "error" in error_data:
                error_msg = error_data["error"]
        except:
            error_msg = response.text or f"HTTP error: {response.status_code}"
        raise SSOServerError(error_msg)
    return response.json()


def get_jwt_by_refresh(token: str) -> dict[str, Any]:
    """Exchange refresh token for JWT tokens.

    Args:
        token (str): refresh token from SSO

    Raises:
        SSOServerError: If SSO server returns an error

    Returns:
        dict[str, Any]: payload with JWT tokens
    """
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": token,
        "client_id": settings.SSO_CLIENT_ID,
        "client_secret": settings.SSO_CLIENT_SECRET,
    }
    response = requests.post(
        settings.SSO_TOKEN_URL,
        data=payload,
        timeout=20,
    )
    if response.status_code != HTTPStatus.OK:
        error_msg = "Unknown error"
        try:
            error_data = response.json()
            if "error_description" in error_data:
                error_msg = error_data["error_description"]
            elif "error" in error_data:
                error_msg = error_data["error"]
        except:
            error_msg = response.text or f"HTTP error: {response.status_code}"
        raise SSOServerError(error_msg)
    return response.json()

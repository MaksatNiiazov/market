"""Example entry point demonstrating how to switch between real and mocked SSO."""

import os

from sso import client, mock_client


def authenticate(username: str, password: str) -> dict:
    """Authenticate using the real or mocked SSO client.

    Set environment variable ``USE_MOCK_SSO`` to ``"true"`` to enable the
    mocked client.
    """
    use_mock = os.getenv("USE_MOCK_SSO", "false").lower() == "true"
    if use_mock:
        return mock_client.authenticate(username, password)
    return client.authenticate(username, password)


def main() -> None:
    """Run a simple authentication flow."""
    username = input("Username: ")
    password = input("Password: ")

    try:
        token = authenticate(username, password)
    except NotImplementedError as exc:
        print(f"Authentication failed: {exc}")
    else:
        print(f"Authenticated as {token['user']}. Token: {token['access_token']}")


if __name__ == "__main__":
    main()

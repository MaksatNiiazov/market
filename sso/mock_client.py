"""Mock SSO client for local testing.

This module simulates an SSO provider and always returns a pre-defined token.
Use it when you need to run the application without access to the real SSO.
"""

TOKEN = "test-token"


def authenticate(username: str, password: str) -> dict:
    """Return a static token as if the user was authenticated."""
    return {"access_token": TOKEN, "user": username}

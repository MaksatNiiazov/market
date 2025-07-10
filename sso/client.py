"""Real SSO client placeholder.
In production this module would handle authentication against the real SSO provider.
"""


def authenticate(username: str, password: str) -> dict:
    """Authenticate user against real SSO provider.

    This function is a placeholder and should be replaced with actual
    SSO client logic. It raises ``NotImplementedError`` to indicate
    that real authentication is not implemented for this example.
    """
    raise NotImplementedError("SSO authentication not implemented")

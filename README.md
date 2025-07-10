# Market

This repository contains a minimal example demonstrating how to mock an
SSO (Single Sign-On) client for local testing. The real SSO client is left
unimplemented; instead, you can enable a mocked version that always returns
a static token.

## Usage

1. Install Python 3.10+.
2. Run the example application:

```bash
# use mock SSO
export USE_MOCK_SSO=true
python main.py
```

When `USE_MOCK_SSO` is set to `true`, authentication will succeed using the
mock client. Without this variable, the real client will raise
`NotImplementedError`.

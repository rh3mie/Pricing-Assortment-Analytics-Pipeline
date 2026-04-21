from __future__ import annotations

import requests
from scripts.config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL, validate_config


def get_access_token() -> str:
    validate_config()

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "scope": "product.compact",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()
    token = payload.get("access_token")

    if not token:
        raise RuntimeError(f"Token response missing access_token: {payload}")

    return token
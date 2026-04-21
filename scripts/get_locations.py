from __future__ import annotations

from typing import Any
import requests

from scripts.config import LOCATIONS_URL, ZIP_CODE, LOCATION_LIMIT


def fetch_locations(access_token: str) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "filter.zipCode.near": ZIP_CODE,
        "filter.radiusInMiles": 10,
        "filter.limit": LOCATION_LIMIT,
    }

    response = requests.get(
        LOCATIONS_URL,
        headers=headers,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def extract_location_ids(location_payload: dict[str, Any]) -> list[str]:
    return [
        item["locationId"]
        for item in location_payload.get("data", [])
        if item.get("locationId")
    ]
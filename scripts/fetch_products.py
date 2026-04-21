from __future__ import annotations

from typing import Any
import json
from pathlib import Path
import time
import requests

from scripts.config import PRODUCTS_URL, PRODUCT_LIMIT, RAW_DIR


def fetch_products_for_term(
    access_token: str,
    search_term: str,
    location_id: str,
    max_retries: int = 3,
    retry_delay: int = 3,
) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "filter.term": search_term,
        "filter.locationId": location_id,
        "filter.limit": PRODUCT_LIMIT,
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                PRODUCTS_URL,
                headers=headers,
                params=params,
                timeout=30,
            )

            if response.status_code == 503:
                print(
                    f"503 error for term='{search_term}', location='{location_id}' "
                    f"(attempt {attempt}/{max_retries}). Retrying in {retry_delay}s..."
                )
                time.sleep(retry_delay)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(
                f"Request failed for term='{search_term}', location='{location_id}' "
                f"(attempt {attempt}/{max_retries}): {e}"
            )
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                print(f"Skipping term='{search_term}' after {max_retries} failed attempts.")
                return {"data": []}

    return {"data": []}


def save_raw_payload(payload: dict[str, Any], filename: str) -> Path:
    out_path = RAW_DIR / filename
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return out_path
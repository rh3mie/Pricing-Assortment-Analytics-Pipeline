from __future__ import annotations

from typing import Any
from datetime import date
from pathlib import Path

import pandas as pd

from scripts.config import PROCESSED_DIR
from scripts.parse_size import parse_size, convert_to_base_unit


def _safe_get_list_value(values: list[Any], index: int) -> Any:
    if not isinstance(values, list) or len(values) <= index:
        return None
    return values[index]


def flatten_products(
    payload: dict[str, Any],
    search_term: str,
    location_id: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    run_date = date.today().isoformat()

    for product in payload.get("data", []):
        items = product.get("items", [])
        categories = product.get("categories", [])

        if not items:
            rows.append(
                {
                    "run_date": run_date,
                    "search_term": search_term,
                    "location_id": location_id,
                    "product_id": product.get("productId"),
                    "upc": product.get("upc"),
                    "product_name": product.get("description"),
                    "brand": product.get("brand"),
                    "category": _safe_get_list_value(categories, 0),
                    "sub_category": _safe_get_list_value(categories, 1),
                    "country_origin": product.get("countryOrigin"),
                    "temperature_indicator": product.get("temperature", {}).get("indicator"),
                    "item_id": None,
                    "regular_price": None,
                    "promo_price": None,
                    "effective_price": None,
                    "discount_pct": None,
                    "size": None,
                    "unit_size": None,
                    "unit_type": None,
                    "base_unit_size": None,
                    "base_unit_type": None,
                    "price_per_unit": None,
                    "sold_by": None,
                    "stock_level": None,
                    "availability": None,
                    "price_source": "kroger_api",
                }
            )
            continue

        for item in items:
            price = item.get("price", {})
            inventory = item.get("inventory", {})
            fulfillment = item.get("fulfillment", {})

            regular_price = price.get("regular")
            promo_price = price.get("promo")
            effective_price = promo_price if promo_price not in (None, 0) else regular_price

            discount_pct = None
            if regular_price not in (None, 0) and promo_price not in (None, 0):
                discount_pct = round((regular_price - promo_price) / regular_price, 4)

            raw_size = item.get("size")
            unit_size, unit_type = parse_size(raw_size)
            base_unit_size, base_unit_type = convert_to_base_unit(unit_size, unit_type)

            price_per_unit = None
            if effective_price not in (None, 0) and base_unit_size not in (None, 0):
                price_per_unit = round(effective_price / base_unit_size, 4)

            rows.append(
                {
                    "run_date": run_date,
                    "search_term": search_term,
                    "location_id": location_id,
                    "product_id": product.get("productId"),
                    "upc": product.get("upc"),
                    "product_name": product.get("description"),
                    "brand": product.get("brand"),
                    "category": _safe_get_list_value(categories, 0),
                    "sub_category": _safe_get_list_value(categories, 1),
                    "country_origin": product.get("countryOrigin"),
                    "temperature_indicator": product.get("temperature", {}).get("indicator"),
                    "item_id": item.get("itemId"),
                    "regular_price": regular_price,
                    "promo_price": promo_price,
                    "effective_price": effective_price,
                    "discount_pct": discount_pct,
                    "size": raw_size,
                    "unit_size": unit_size,
                    "unit_type": unit_type,
                    "base_unit_size": base_unit_size,
                    "base_unit_type": base_unit_type,
                    "price_per_unit": price_per_unit,
                    "sold_by": item.get("soldBy"),
                    "stock_level": inventory.get("stockLevel"),
                    "availability": fulfillment.get("curbside"),
                    "price_source": "kroger_api",
                }
            )

    return pd.DataFrame(rows)


def append_or_create_csv(df: pd.DataFrame, filename: str = "kroger_products.csv") -> Path:
    out_path = PROCESSED_DIR / filename

    if out_path.exists():
        existing = pd.read_csv(out_path)
        combined = pd.concat([existing, df], ignore_index=True)
        combined.drop_duplicates(
            subset=["run_date", "location_id", "search_term", "product_id", "item_id"],
            inplace=True,
        )
        combined.to_csv(out_path, index=False)
    else:
        df.to_csv(out_path, index=False)

    return out_path
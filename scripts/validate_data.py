from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "run_date",
    "search_term",
    "location_id",
    "product_id",
    "product_name",
    "brand",
    "regular_price",
]


def validate_dataframe(df: pd.DataFrame) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if df.empty:
        errors.append("Validation failed: dataframe is empty.")
        return False, errors

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    if "product_id" in df.columns:
        missing_product_ids = df["product_id"].isna().sum()
        if missing_product_ids > 0:
            errors.append(f"Missing product_id values: {missing_product_ids}")

    if "product_name" in df.columns:
        missing_product_names = df["product_name"].isna().sum()
        if missing_product_names > 0:
            errors.append(f"Missing product_name values: {missing_product_names}")

    if "regular_price" in df.columns:
        missing_prices = df["regular_price"].isna().sum()
        price_missing_pct = missing_prices / len(df)
        if price_missing_pct > 0.5:
            errors.append(
                f"Too many missing regular_price values: {missing_prices} of {len(df)} rows "
                f"({price_missing_pct:.1%})."
            )

        negative_prices = (df["regular_price"].fillna(0) < 0).sum()
        if negative_prices > 0:
            errors.append(f"Negative regular_price values found: {negative_prices}")

    if "promo_price" in df.columns and "regular_price" in df.columns:
        invalid_promo = (
            (df["promo_price"].notna()) &
            (df["regular_price"].notna()) &
            (df["promo_price"] > df["regular_price"])
        ).sum()
        if invalid_promo > 0:
            errors.append(
                f"Found {invalid_promo} rows where promo_price is greater than regular_price."
            )

    if {"run_date", "location_id", "search_term", "product_id", "item_id"}.issubset(df.columns):
        duplicate_count = df.duplicated(
            subset=["run_date", "location_id", "search_term", "product_id", "item_id"]
        ).sum()
        if duplicate_count > 0:
            errors.append(f"Duplicate rows found: {duplicate_count}")
    if "effective_price" in df.columns:
        missing_effective = df["effective_price"].isna().sum()
        if missing_effective > 0:
            errors.append(f"Missing effective_price values: {missing_effective}")

    if "price_per_unit" in df.columns:
        missing_ppu = df["price_per_unit"].isna().sum()
    if missing_ppu / len(df) > 0.7:
        errors.append(
            f"Too many missing price_per_unit values: {missing_ppu} of {len(df)} rows."
        )

    return len(errors) == 0, errors


from __future__ import annotations

from datetime import datetime
import time
import pandas as pd

from scripts.auth import get_access_token
from scripts.config import SEARCH_TERM_MAP
from scripts.get_locations import fetch_locations, extract_location_ids
from scripts.fetch_products import fetch_products_for_term, save_raw_payload
from scripts.transform_products import flatten_products, append_or_create_csv
from scripts.validate_data import validate_dataframe


def main() -> None:
    print("Starting Kroger pipeline...")

    token = get_access_token()

    location_payload = fetch_locations(token)
    location_ids = extract_location_ids(location_payload)

    if not location_ids:
        raise RuntimeError("No Kroger locations found for the configured ZIP code.")

    print(f"Found location IDs: {location_ids}")

    frames: list[pd.DataFrame] = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for location_id in location_ids:
        for group_name, terms in SEARCH_TERM_MAP.items():
            for term in terms:
                print(f"Fetching group='{group_name}' term='{term}' for location='{location_id}'")

                payload = fetch_products_for_term(
                    access_token=token,
                    search_term=term,
                    location_id=location_id,
                )

                raw_name = f"products_{group_name}_{term}_{location_id}_{timestamp}.json".replace(" ", "_")
                save_raw_payload(payload, raw_name)

                df = flatten_products(
                    payload=payload,
                    search_term=term,
                    location_id=location_id,
                )

                df["search_group"] = group_name

                print(f"  Retrieved {len(df)} rows")
                frames.append(df)

                time.sleep(1)

    final_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    print(f"Total rows before validation: {len(final_df)}")

    is_valid, validation_errors = validate_dataframe(final_df)

    if not is_valid:
        print("\nValidation warnings:")
        for err in validation_errors:
            print(f" - {err}")
        print("Continuing pipeline despite validation warnings.")

    csv_path = append_or_create_csv(final_df)

    print("\nPipeline finished.")
    print(f"Wrote {len(final_df)} rows to {csv_path}")


if __name__ == "__main__":
    main()
# Pricing & Assortment Analytics Pipeline

*By Rhey Mar De Vera*

## Overview
This project simulates a real-world retail analytics workflow by collecting product-level pricing and assortment data across multiple categories and store locations via the Kroger Product API.

The goal is to analyze:
- Pricing trends across product categories
- Promotional activity and discount patterns
- Brand-level pricing differences
- Product assortment variation across stores

**Technical Tools Used:**
- Python
- Kroger Product API
- Tableau Public

**Data Pipeline**

Kroger API -> Python ETL -> Processed CSV -> Tableau Dashboard

## The Data

The dataset was extracted from the API on 4/16/25 and contained 9000+ product records across multiple categories. The dataset volume will change over time based on the run date and real-world changes, but the key fields will remain the same.

Key Fields:
- ```product_id```, ```product_name```, ```brand```
- ```category```, ```sub_category```, ```search_group```
- ```regular_price```, ```promo_price```, ```effective_price```
- ```discount_pct```
- ```unit_size```, ```unit_type```, ```price_per_unit```
- ```location_id```

## Data Processing

Key Transformations:
- Flattened nested API responses into a structured tabular CSV format, making it usable for analysis
- Created ```effective_price``` to standardize pricing logic based on regular price and discounts at the time
- Added ```discount_pct``` to analyze promotions
- Parsed product size into numeric fields for better comparable base units
- Calculated ```price_per_unit``` for fair price comparison
- Tagged products with ```search_group``` for category-level analysis

## Data Validation

Added ```validate_data.py``` script to ensure data quality from API extractions. These checks included:

- Checking for required fields (product_id. price, etc.)
- Missing and invalid price detection (negative values, null, etc)
- Duplicate record checks
- Logical validation (promo_price <= regular_price)

## Tableau Dashboard
<img width="1363" height="764" alt="image" src="https://github.com/user-attachments/assets/e12ad41c-f414-410a-8adb-5de84e5c5f07" />


## Automation

The pipeline is automated using a scheduled Python script that:

- Extracts updated product data from the API
- Rebuilds the dataset
- Outputs an updated CSV for Tableau

This can be further automated by using scheduling tools such as Task Scheduler to run the script daily, or by connecting it to a cloud database (Tableau Public doesn't support this).

## Key Takeaways

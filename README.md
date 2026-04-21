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

The dataset was extracted from the API on 4/16/26 and contained 9000+ product records across multiple categories. The dataset volume will change over time based on the run date and real-world changes, but the key fields will remain the same.

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

[View Live Dashboard Here](https://public.tableau.com/views/pricing_and_assortment_analytics_dashboard/PricingandAssortmentAnalyticsDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

This dashboard consists of 5 interactive visualizations connected by global filters (Search Group, Stock Level, Temperature Indicator, Availability)

- **Inventory Status by Product Group** — 100% stacked bar showing 
  stock level distribution (HIGH/LOW/OUT OF STOCK) across all 9 
  search groups
- **Price vs. Cost Per Unit by Storage Type** — scatter plot revealing 
  the relationship between regular price and unit economics, colored 
  by storage type (Ambient/Frozen/Refrigerated)
- **Avg Price Per Unit by Category** — horizontal bar chart ranking 
  categories by unit cost, highlighting premium vs. budget segments
- **Availability Heatmap** — cross-tabulation of search group vs. 
  storage type showing availability rates
- **Promotional Discount Distribution by Product Group** — box plot 
  showing discount % spread per group, revealing which categories 
  run the deepest and most consistent promotions

## Automation

The pipeline is automated using a scheduled Python script that:

- Extracts updated product data from the API
- Rebuilds the dataset
- Outputs an updated CSV for Tableau

This can be further automated by using scheduling tools such as Task Scheduler to run the script daily, or by connecting it to a cloud database (Tableau Public doesn't support this).

## Key Takeaways

**Pricing**
- The average regular price across 7,808 products is $6.47
- Personal Care ($2.90), Bakery ($2.41), and Beauty ($1.79) have 
  the highest average price per unit
- The scatter plot shows the majority of products cluster under $5 
  regular price and an under $2 price per unit, with Ambient products 
  (purple) spanning the widest price range
- Refrigerated and Frozen products are tightly clustered in the 
  lower-left, confirming they are consistently lower-cost per unit

**Promotions**
- 41.05% of products have an active promotional price at the time 
  of extraction
- Discount % is remarkably consistent across all 9 search groups, 
  with medians ranging narrowly between 17–22%
- Protein shows the widest discount spread (largest IQR box), 
  meaning promotional depth is least predictable in that category
- Nearly all groups have outliers reaching 50–60% discount, 
  suggesting opportunistic deep discounting exists across the 
  entire store

**Inventory & Availability**
- 80.62% of products are HIGH stock at the time of extraction, 
  indicating strong overall inventory health
- Produce and Beverages carry the largest OUT OF STOCK segments 
  in the stacked bar, making them the highest-risk categories 
  for stockouts
- Pantry leads availability at 53% Ambient, while Frozen products 
  show strong availability (53–67%) across most groups
- Household has the smallest out-of-stock proportion, suggesting 
  the most stable replenishment among all groups

**Assortment**
- The catalog spans 9 search groups with Pantry, Dairy, and 
  Beverages being the most represented based on the heatmap coverage
- Availability rates vary meaningfully by storage type. Frozen 
  availability (53–67%) consistently outperforms Refrigerated 
  (42–50%) across most search groups
- Several Household and Snacks cells are blank in the heatmap, 
  indicating those groups carry little to no Frozen inventory, 
  which is expected given their category nature

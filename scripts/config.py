from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

CLIENT_ID = os.getenv("KROGER_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET", "").strip()
ZIP_CODE = os.getenv("KROGER_ZIP_CODE", "20852").strip()

SEARCH_TERMS = [
    term.strip()
    for term in os.getenv("KROGER_SEARCH_TERMS", "").split(",")
    if term.strip()
]

SEARCH_TERM_MAP = {
    "Dairy": [
        "milk", "eggs", "yogurt", "cheese", "butter",
        "cream", "sour cream", "cottage cheese", "cream cheese"
    ],
    "Pantry": [
        "bread", "pasta", "rice", "cereal", "coffee",
        "flour", "sugar", "oats", "peanut butter", "jam"
    ],
    "Beverages": [
        "juice", "soda", "water", "sparkling water",
        "energy drink", "sports drink", "tea"
    ],
    "Produce": [
        "apples", "bananas", "oranges", "grapes",
        "strawberries", "blueberries", "spinach",
        "broccoli", "carrots", "lettuce"
    ],
    "Protein": [
        "chicken", "beef", "ground beef", "pork",
        "salmon", "tuna", "shrimp", "turkey"
    ],
    "Snacks": [
        "chips", "crackers", "cookies", "granola bars",
        "popcorn", "pretzels", "nuts"
    ],
    "Frozen": [
        "frozen pizza", "frozen meals", "ice cream",
        "frozen vegetables", "frozen chicken"
    ],
    "Household": [
        "paper towels", "toilet paper", "dish soap",
        "laundry detergent", "cleaning spray"
    ],
    "Breakfast": [
        "pancake mix", "waffles", "maple syrup",
        "breakfast bars"
    ]
}

LOCATION_LIMIT = int(os.getenv("KROGER_LOCATION_LIMIT", "3"))
PRODUCT_LIMIT = int(os.getenv("KROGER_PRODUCT_LIMIT", "50"))

TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"
LOCATIONS_URL = "https://api.kroger.com/v1/locations"
PRODUCTS_URL = "https://api.kroger.com/v1/products"


def validate_config() -> None:
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(
            "Missing Kroger credentials. Set KROGER_CLIENT_ID and KROGER_CLIENT_SECRET in .env"
        )
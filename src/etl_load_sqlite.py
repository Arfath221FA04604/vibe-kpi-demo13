"""Load the sample customer CSV into a local SQLite database."""

import sqlite3
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT_DIR / "data" / "raw" / "customers_raw.csv"
DB_PATH = ROOT_DIR / "data" / "db" / "analytics.db"


def main() -> None:
    """Create the database table and replace it with rows from the CSV."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    customers = pd.read_csv(CSV_PATH)
    with sqlite3.connect(DB_PATH) as connection:
        customers.to_sql("customers_raw", connection, if_exists="replace", index=False)
    print(f"Loaded {len(customers)} customer rows into {DB_PATH}")


if __name__ == "__main__":
    main()

"""Calculate simple customer KPIs for one city."""

import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "db" / "analytics.db"


def city_kpi(city: str) -> dict[str, float | int | str] | None:
    """Print and return customer count, average spend, and churn count for a city."""
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            """SELECT city, COUNT(*), AVG(monthly_spend), SUM(churned)
               FROM customers_raw WHERE city = ? GROUP BY city""",
            (city,),
        ).fetchone()
    if row is None:
        print(f"No customer data found for city: {city}")
        return None
    result = {
        "city": row[0],
        "customer_count": row[1],
        "average_monthly_spend": row[2],
        "churned_count": row[3],
    }
    print(result)
    return result


if __name__ == "__main__":
    city_kpi("Mumbai")
    city_kpi("Mumbai' OR 1=1 --")

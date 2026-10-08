"""Tests for the city KPI query."""

import sqlite3

import pytest

from src import kpi_city


@pytest.fixture
def sample_database(tmp_path, monkeypatch):
    """Create isolated sample data for a test."""
    db_path = tmp_path / "analytics.db"
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE customers_raw (customer_id INTEGER, city TEXT, monthly_spend REAL, churned INTEGER)")
        connection.executemany(
            "INSERT INTO customers_raw VALUES (?, ?, ?, ?)",
            [(1, "Mumbai", 1200.0, 0), (2, "Mumbai", 800.0, 1), (3, "Delhi", 500.0, 0)],
        )
    monkeypatch.setattr(kpi_city, "DB_PATH", db_path)
    return db_path


def test_city_kpi_returns_expected_mumbai_summary(sample_database, capsys):
    result = kpi_city.city_kpi("Mumbai")
    assert result["city"] == "Mumbai"
    assert result["customer_count"] == 2
    assert result["average_monthly_spend"] == pytest.approx(1000.0)
    assert result["churned_count"] == 1
    assert "Mumbai" in capsys.readouterr().out


def test_injection_attempt_does_not_return_all_rows(sample_database, capsys):
    result = kpi_city.city_kpi("Mumbai' OR 1=1 --")
    assert result is None
    assert "No customer data found" in capsys.readouterr().out

# Applied Analytics Mini Project

A beginner friendly example that loads customer CSV data into SQLite and calculates city level KPIs.

## Run the project

Run these commands from the repository root after activating `.venv`:

```powershell
python -m pip install -r requirements.txt
python src/etl_load_sqlite.py
python src/kpi_city.py
python -m pytest
```

The KPI script prints results for Mumbai and for a SQL injection attempt. The second call safely returns no matching city.

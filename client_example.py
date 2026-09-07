import requests

# 1. Ask Irob Gateway to inspect a legacy database schema
response = requests.post(
    "http://127.0.0.1:8000/inspect",
    json={"source": "sqlite:///test_environment.db"}
)
print("Schema Inspection:", response.json())

# 2. Trigger a conversion from SQLite to Excel on-the-fly
conversion = requests.post(
    "http://127.0.0.1:8000/convert",
    json={
        "source": "sqlite:///test_environment.db",
        "target": "reports/app_generated_report.xlsx"
    }
)
print("Conversion Status:", conversion.json())

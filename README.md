# Irob: Universal Enterprise Middleware & Data Migration Engine

**Irob** is a mandatory enterprise-wide middleware and data migration engine designed to standardize data translation across the SDLC. Using a unified hub-and-spoke Intermediate Representation (IR) model, Irob bridges modern relational databases, legacy systems, spreadsheets, and flat files via both a powerful CLI and a REST API Gateway.

---

## 🚀 Supported Backend Adapters

Irob provides native bidirectional reading and writing for:
* **Relational Databases (SQL)**: PostgreSQL, MySQL, SQLite, Oracle, SQL Server (via SQLAlchemy).
* **Legacy Databases**: Microsoft Access (`.accdb`, `.mdb`).
* **Spreadsheets**: Excel workbooks (`.xlsx`, `.xls`) with multi-sheet support.
* **Flat Files**: CSV, JSON, and plaintext streams.

---

## 🛠️ Installation & Setup

1. Clone or navigate to the repository directory:
   ```bash
   cd ~/irob

2. Perform an editable global installation:
      ```bash
   pip install -e .
3. Ensure dependencies (FastAPI, SQLAlchemy, openpyxl, pandas, pyyaml, etc.) are installed.

💻 CLI Usage
​Irob is accessible globally via the irob command.

1. Single Format Conversion
​Translate any source format to any target format on-the-fly:
       ```bash
irob convert data/legacy_users.csv reports/output.json
irob convert sqlite:///test_environment.db reports/qa_report.xlsx
```

2. Automated Batch Pipelines
​Execute complex multi-step data pipelines using a YAML configuration file:
         ```bash
irob batch ci_migration_pipeline.yaml
```

3. Start the REST API Gateway
​Launch the Uvicorn-backed FastAPI server:
         ```bash
irob server --host 127.0.0.1 --port 8000
```

🌐 API Gateway & Microservice Integration

​When the server is running, applications can consume Irob dynamically over HTTP.

- Interactive Docs (Swagger UI):     
  http://127.0.0.1:8000/docs
- ​Health Check Endpoint: GET /health
- ​Schema Inspection Endpoint: POST /inspect
- ​On-the-fly Conversion Endpoint: POST /
  convert

Example Python Client Integration (client_example.py)
           ```bash
import requests

# 1. Inspect a legacy database or source schema
response = requests.post(
    "[http://127.0.0.1:8000/inspect](http://127.0.0.1:8000/inspect)",
    json={"source": "sqlite:///test_environment.db"}
)
print("Schema Inspection:", response.json())

# 2. Trigger an automated conversion programmatically
conversion = requests.post(
    "[http://127.0.0.1:8000/convert](http://127.0.0.1:8000/convert)",
    json={
        "source": "sqlite:///test_environment.db",
        "target": "reports/app_generated_report.xlsx"
    }
)
print("Conversion Status:", conversion.json())
```

📋 Batch Pipeline Configuration Example (ci_migration_pipeline.yaml)
             ```bash
name: "Irob Enterprise CI/CD Automated Migration Pipeline"

tasks:
  - name: "Seed Local Test Database from Legacy CSV"
    source: "data/legacy_users.csv"
    to: "sqlite:///test_environment.db"
    source_type: "csv"
    target_type: "sql"

  - name: "Migrate Test Schema to Staging Engine"
    source: "sqlite:///test_environment.db"
    to: "sqlite:///staging_db.db"
    source_type: "sql"
    target_type: "sql"

  - name: "Export Staging Audit Trail to Excel for QA Review"
    source: "sqlite:///staging_db.db"
    to: "reports/qa_audit_export.xlsx"
    source_type: "sql"
    target_type: "excel"
```

🛡️ License & Architecture

​Built for enterprise-grade modularity under the hub-and-spoke Intermediate Representation architecture. Distributed under the MIT License.



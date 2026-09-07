import csv
import json
from pathlib import Path

class EtcWriter:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def write(self, ir_data):
        ext = self.file_path.suffix.lower()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Flatten multi-table IR to single file or primary table if JSON/CSV
        primary_table = list(ir_data.keys())[0] if ir_data else "data"
        rows = ir_data.get(primary_table, [])

        if ext == '.json':
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(rows, f, indent=4)
        elif ext in ('.csv', '.txt'):
            if rows:
                with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
        print(f"Successfully exported to file target: {self.file_path}")

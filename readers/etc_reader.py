import csv
import json
from pathlib import Path

class EtcReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def read(self):
        ext = self.file_path.suffix.lower()
        table_name = self.file_path.stem
        rows = []

        if ext == '.json':
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                rows = data if isinstance(data, list) else [data]
        elif ext in ('.csv', '.txt'):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = [row for row in reader]
        else:
            raise ValueError(f"Unsupported file format for EtcReader: {ext}")

        return {table_name: rows}

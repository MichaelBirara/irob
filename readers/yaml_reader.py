import yaml
from pathlib import Path

class YamlReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read(self) -> dict:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        table_name = self.file_path.stem
        if isinstance(data, list):
            return {table_name: data}
        elif isinstance(data, dict):
            # If it's already a dictionary of tables/lists
            return {k: (v if isinstance(v, list) else [v]) for k, v in data.items()}
        return {table_name: [{"value": data}]}

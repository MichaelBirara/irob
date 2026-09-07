import yaml
from pathlib import Path

class YamlWriter:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def write(self, ir_data: dict):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(ir_data, f, sort_keys=False)
        print(f"Successfully exported to YAML target: {self.file_path}")

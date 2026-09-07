import pandas as pd
from pathlib import Path

class ParquetWriter:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def write(self, ir_data: dict):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        for table_name, rows in ir_data.items():
            if not rows:
                continue
            df = pd.DataFrame(rows)
            target = self.file_path if len(ir_data) == 1 else self.file_path.with_name(f"{self.file_path.stem}_{table_name}{self.file_path.suffix}")
            df.to_parquet(target, index=False)
            print(f"Successfully exported to Parquet target: {target}")

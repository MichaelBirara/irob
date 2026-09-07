import pandas as pd
from pathlib import Path

class ParquetReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read(self) -> dict:
        df = pd.read_parquet(self.file_path)
        table_name = self.file_path.stem
        return {table_name: df.to_dict(orient="records")}

import xml.etree.ElementTree as ET
from pathlib import Path

class XMLReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def read(self) -> dict:
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        table_name = self.file_path.stem
        rows = []
        for child in root:
            row = {elem.tag: elem.text for elem in child}
            rows.append(row)
        if not rows and root.text:
            rows = [{"value": root.text}]
        return {table_name: rows}

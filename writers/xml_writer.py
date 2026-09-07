import xml.etree.ElementTree as ET
from pathlib import Path

class XMLWriter:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def write(self, ir_data: dict):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        for table_name, rows in ir_data.items():
            if not rows:
                continue
            root = ET.Element("root")
            for row in rows:
                item_elem = ET.SubElement(root, "record")
                for k, v in row.items():
                    sub = ET.SubElement(item_elem, str(k))
                    sub.text = str(v) if v is not None else ""
            tree = ET.ElementTree(root)
            target = self.file_path if len(ir_data) == 1 else self.file_path.with_name(f"{self.file_path.stem}_{table_name}.xml")
            tree.write(target, encoding="utf-8", xml_declaration=True)
            print(f"Successfully exported to XML target: {target}")

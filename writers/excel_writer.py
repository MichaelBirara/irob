from pathlib import Path
import openpyxl

class ExcelWriter:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def write(self, ir_data):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        wb = openpyxl.Workbook()
        
        # Remove default sheet created by workbook
        default_sheet = wb.active
        wb.remove(default_sheet)

        for table_name, rows in ir_data.items():
            # Excel sheet names have a 31-character limit
            safe_sheet_name = table_name[:31] if table_name else "sheet"
            sheet = wb.create_sheet(title=safe_sheet_name)
            
            if not rows:
                continue
            
            headers = list(rows[0].keys())
            sheet.append(headers)
            
            for row in rows:
                sheet.append([row.get(h) for h in headers])

        wb.save(self.file_path)
        print(f"Successfully exported to Excel target: {self.file_path}")

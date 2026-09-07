from pathlib import Path

try:
    from access_parser import AccessParser as AccessDB
except ImportError:
    try:
        from access_parser import AccessDB
    except ImportError:
        AccessDB = None

class AccessReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def read(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Access database not found: {self.file_path}")
        
        if AccessDB is None:
            raise ImportError("The 'access-parser' library is not properly configured.")
        
        db = AccessDB(str(self.file_path))
        ir_data = {}
        
        catalog = getattr(db, 'catalog', {})
        for table_name in catalog.keys():
            try:
                rows = []
                table_data = db.parse_table(table_name)
                for record in table_data:
                    rows.append(dict(record))
                ir_data[table_name] = rows
            except Exception as e:
                print(f"Warning: Could not parse Access table '{table_name}': {e}")
                
        return ir_data

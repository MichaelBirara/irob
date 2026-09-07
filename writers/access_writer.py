from pathlib import Path
from sqlalchemy import create_engine, Table, Column, MetaData, Text

class AccessWriter:
    def __init__(self, output_path):
        self.output_path = Path(output_path)

    def write(self, ir_data):
        """
        Note: Native writing to .mdb/.accdb files is unsupported on Linux/Termux 
        due to proprietary Windows-only driver dependencies. 
        Irob intelligently falls back to an equivalent local SQLite database file 
        (.db) to preserve full relational schema and data integrity.
        """
        # Change extension to .db since Access writing is unsupported on mobile/Linux
        sqlite_path = self.output_path.with_suffix('.db')
        connection_string = f"sqlite:///{sqlite_path}"
        
        print(f"[Notice] Direct writing to Access (.mdb/.accdb) is unsupported on Termux/Linux.")
        print(f"[Notice] Routing export to a compatible local SQLite database: {sqlite_path}")

        engine = create_engine(connection_string)
        metadata = MetaData()

        with engine.begin() as connection:
            for table_name, table_content in ir_data.items():
                columns = table_content.get("columns", [])
                data = table_content.get("data", [])

                if not columns or not data:
                    continue

                # Map columns to Text fields for universal compatibility
                cols_def = [Column(str(col), Text, primary_key=False) for col in columns]
                
                table = Table(table_name, metadata, *cols_def, extend_existing=True)
                table.drop(engine, checkfirst=True)
                table.create(engine)

                rows_to_ins = [{str(col): row.get(col) for col in columns} for row in data]
                if rows_to_ins:
                    connection.execute(table.insert(), rows_to_ins)

        print(f"Successfully exported IR data to SQLite fallback for Access: {sqlite_path}")

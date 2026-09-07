from sqlalchemy import create_engine, text

class SQLWriter:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)

    def write(self, ir_data: dict):
        if not ir_data or not isinstance(ir_data, dict):
            raise ValueError("SQLWriter expected a dictionary Intermediate Representation (IR).")

        with self.engine.begin() as connection:
            for table_name, rows in ir_data.items():
                if not rows:
                    print(f"Notice: Table '{table_name}' has no rows to write. Skipping.")
                    continue
                
                # Drop and recreate / insert rows using pure SQL / SQLAlchemy
                try:
                    # Simple table recreation strategy
                    keys = rows[0].keys()
                    columns_def = ", ".join([f'"{k}" TEXT' for k in keys])
                    connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                    connection.execute(text(f"CREATE TABLE {table_name} ({columns_def})"))
                    
                    placeholders = ", ".join([f":{k}" for k in keys])
                    cols_insert = ", ".join([f'"{k}"' for k in keys])
                    insert_stmt = text(f"INSERT INTO {table_name} ({cols_insert}) VALUES ({placeholders})")
                    
                    connection.execute(insert_stmt, rows)
                    print(f"Successfully wrote {len(rows)} rows to table '{table_name}' in SQL target.")
                except Exception as e:
                    raise RuntimeError(f"Failed to write table '{table_name}' to SQL target: {e}")
        
        print("Successfully exported IR data to database target.")

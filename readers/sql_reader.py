from sqlalchemy import create_engine, inspect, text

class SQLReader:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)

    def read(self) -> dict:
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        ir_data = {}

        with self.engine.connect() as connection:
            for table_name in tables:
                try:
                    result = connection.execute(text(f"SELECT * FROM {table_name}"))
                    rows = [dict(row._mapping) for row in result]
                    ir_data[table_name] = rows
                except Exception as e:
                    print(f"Warning: Could not read table '{table_name}' from SQL source: {e}")

        return ir_data

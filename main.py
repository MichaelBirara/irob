import sys
import argparse
import yaml
from pathlib import Path

def detect_type(source: str) -> str:
    src = str(source).lower()
    if src.startswith(("sqlite://", "postgresql://", "mysql://", "oracle://", "sqlserver://")):
        return "sql"
    if src.startswith(("mongodb://", "mongodb+srv://")):
        return "mongodb"
    
    ext = Path(source).suffix.lower()
    if ext in (".csv",):
        return "csv"
    elif ext in (".json",):
        return "json"
    elif ext in (".parquet", ".pq"):
        return "parquet"
    elif ext in (".xml",):
        return "xml"
    elif ext in (".yaml", ".yml"):
        return "yaml"
    elif ext in (".xlsx", ".xls"):
        return "excel"
    elif ext in (".accdb", ".mdb"):
        return "access"
    elif ext in (".txt",):
        return "txt"
    else:
        return "sql"

def get_reader(source: str, source_type: str):
    st = source_type.lower()
    if st in ("sql", "database"):
        from readers.sql_reader import SQLReader
        return SQLReader(source)
    elif st in ("mongodb", "mongo", "nosql"):
        from readers.mongo_reader import MongoReader
        return MongoReader(source)
    elif st in ("access", "mdb", "accdb"):
        from readers.access_reader import AccessReader
        return AccessReader(source)
    elif st in ("excel", "xlsx", "xls"):
        from readers.excel_reader import ExcelReader
        return ExcelReader(source)
    elif st in ("parquet", "pq"):
        from readers.parquet_reader import ParquetReader
        return ParquetReader(source)
    elif st in ("xml",):
        from readers.xml_reader import XMLReader
        return XMLReader(source)
    elif st in ("yaml", "yml"):
        from readers.yaml_reader import YamlReader
        return YamlReader(source)
    elif st in ("csv", "json", "txt", "etc"):
        from readers.etc_reader import EtcReader
        return EtcReader(source)
    else:
        raise ValueError(f"Unknown source type: {source_type}")

def get_writer(target: str, target_type: str):
    tt = target_type.lower()
    if tt in ("sql", "database"):
        from writers.sql_writer import SQLWriter
        return SQLWriter(target)
    elif tt in ("mongodb", "mongo", "nosql"):
        from writers.mongo_writer import MongoWriter
        return MongoWriter(target)
    elif tt in ("excel", "xlsx", "xls"):
        from writers.excel_writer import ExcelWriter
        return ExcelWriter(target)
    elif tt in ("parquet", "pq"):
        from writers.parquet_writer import ParquetWriter
        return ParquetWriter(target)
    elif tt in ("xml",):
        from writers.xml_writer import XMLWriter
        return XMLWriter(target)
    elif tt in ("yaml", "yml"):
        from writers.yaml_writer import YamlWriter
        return YamlWriter(target)
    elif tt in ("csv", "json", "txt", "etc"):
        from writers.etc_writer import EtcWriter
        return EtcWriter(target)
    else:
        raise ValueError(f"Unknown target type: {target_type}")

def execute_conversion(source: str, target: str, source_type: str = None, target_type: str = None):
    src_type = source_type or detect_type(source)
    tgt_type = target_type or detect_type(target)

    print(f"  -> Ingesting '{source}' as [{src_type}]...")
    reader = get_reader(source, src_type)
    ir_data = reader.read()

    print(f"  -> Exporting to [{tgt_type}] -> '{target}'...")
    writer = get_writer(target, tgt_type)
    writer.write(ir_data)

def main():
    parser = argparse.ArgumentParser(
        description="Irob: Universal Enterprise Middleware & Data Migration Engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")

    parser_convert = subparsers.add_parser("convert", help="Convert a single source to a target")
    parser_convert.add_argument("source", help="Source file path or connection string")
    parser_convert.add_argument("target", help="Target file path or connection string")
    parser_convert.add_argument("--source-type", help="Explicit source type override")
    parser_convert.add_argument("--target-type", help="Explicit target type override")

    parser_batch = subparsers.add_parser("batch", help="Run multiple migrations via a YAML configuration file")
    parser_batch.add_argument("config", help="Path to batch YAML configuration file")

    parser_server = subparsers.add_parser("server", help="Start the Universal Interpreter Gateway API server")
    parser_server.add_argument("--host", default="127.0.0.1", help="Host to bind server to")
    parser_server.add_argument("--port", type=int, default=8000, help="Port to bind server to")

    args = parser.parse_args()

    if args.command == "convert":
        try:
            execute_conversion(args.source, args.target, args.source_type, args.target_type)
            print("Status: SUCCESS")
        except Exception as e:
            print(f"Status: FAILED -> {e}")
            sys.exit(1)

    elif args.command == "batch":
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Configuration file not found: {config_path}")
            sys.exit(1)
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        tasks = config.get("tasks", [])
        print(f"[Irob] Loaded {len(tasks)} batch task(s) from {args.config}\n")

        success_count = 0
        for idx, task in enumerate(tasks, 1):
            print(f"[{idx}/{len(tasks)}] Running: {task.get('name', 'Unnamed Task')}")
            try:
                execute_conversion(
                    task.get("source"),
                    task.get("to"),
                    task.get("source_type"),
                    task.get("target_type")
                )
                print("Status: SUCCESS\n")
                success_count += 1
            except Exception as e:
                print(f"Status: FAILED -> {e}\n")

        print(f"[Irob] Batch processing finished. ({success_count}/{len(tasks)} successful)")

    elif args.command == "server":
        import uvicorn
        print(f"Starting Irob Universal Interpreter Gateway on {args.host}:{args.port}...")
        uvicorn.run("server:app", host=args.host, port=args.port, reload=True)

if __name__ == "__main__":
    main()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import yaml

from main import detect_type, get_reader, get_writer, execute_conversion

app = FastAPI(
    title="Irob Universal Gateway",
    description="Mandatory Enterprise Middleware & Data Migration Engine",
    version="1.0.0"
)

class ConvertRequest(BaseModel):
    source: str
    target: str
    source_type: Optional[str] = None
    target_type: Optional[str] = None

class InspectRequest(BaseModel):
    source: str
    source_type: Optional[str] = None

class BatchRequest(BaseModel):
    config_path: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "irob-gateway", "version": "1.0.0"}

@app.post("/inspect")
def inspect_source(req: InspectRequest):
    try:
        src_type = req.source_type or detect_type(req.source)
        reader = get_reader(req.source, src_type)
        ir_data = reader.read()
        
        # Summarize IR structure for inspection
        summary = {}
        for table_name, rows in ir_data.items():
            summary[table_name] = {
                "row_count": len(rows),
                "sample_columns": list(rows[0].keys()) if rows and len(rows) > 0 else []
            }
        return {"source": req.source, "detected_type": src_type, "schema_summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, and_detail=str(e))

@app.post("/convert")
def convert_data(req: ConvertRequest):
    try:
        execute_conversion(req.source, req.target, req.source_type, req.target_type)
        return {"status": "success", "message": f"Successfully converted {req.source} to {req.target}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
def run_batch(req: BatchRequest, background_tasks: BackgroundTasks):
    config_path = Path(req.config_path)
    if not config_path.exists():
        raise HTTPException(status_code=404, detail=f"Batch config not found: {config_path}")
    
    def process_batch():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        for task in config.get('tasks', []):
            execute_conversion(
                task.get('source'),
                task.get('to'),
                task.get('source_type'),
                task.get('target_type')
            )

    background_tasks.add_task(process_batch)
    return {"status": "accepted", "message": f"Batch pipeline {req.config_path} queued for execution."}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.lineage import LineageTracker
from src.impact import ImpactAnalyzer
from src.parser import parse_sql_lineage

app = FastAPI(title="Data Lineage API")
tracker = LineageTracker()
analyzer = ImpactAnalyzer(tracker)

class SourceIn(BaseModel):
    table: str
    system: str

class TransformationIn(BaseModel):
    sources: List[str]
    target: str
    job_name: str
    transformation: str

class SQLIn(BaseModel):
    sql: str
    target: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sources")
def add_source(s: SourceIn):
    tracker.register_source(s.table, s.system)
    return {"ok": True}

@app.post("/transformations")
def add_transformation(t: TransformationIn):
    tracker.register_transformation(t.sources, t.target, t.job_name, t.transformation)
    return {"ok": True}

@app.get("/lineage/{table}")
def get_lineage(table: str):
    return tracker.get_lineage(table)

@app.get("/impact/{table}")
def impact(table: str):
    return analyzer.impact_of_change(table)

@app.get("/graph")
def graph():
    return tracker.full_graph()

@app.post("/parse-sql")
def parse_sql(data: SQLIn):
    parsed = parse_sql_lineage(data.sql)
    if parsed["sources"] and data.target:
        tracker.register_transformation(parsed["sources"], data.target,
                                         "parsed_sql", data.sql[:100])
    return parsed

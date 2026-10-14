import re

def parse_sql_lineage(sql):
    """Простой парсер: SELECT ... FROM x JOIN y → target z."""
    sql_lower = sql.lower()
    sources = re.findall(r"(?:from|join)\s+([a-z0-9_\.]+)", sql_lower)
    target = re.search(r"insert\s+into\s+([a-z0-9_\.]+)", sql_lower)
    return {
        "sources": list(set(sources)),
        "target": target.group(1) if target else None,
    }

class ImpactAnalyzer:
    def __init__(self, tracker):
        self.tracker = tracker

    def impact_of_change(self, table, change_type="schema"):
        downstream = self.tracker.lg.downstream(table)
        reports = [n for n in downstream
                   if self.tracker.lg.graph.nodes[n].get("node_type") == "report"]
        tables = [n for n in downstream
                  if self.tracker.lg.graph.nodes[n].get("node_type") == "table"]
        return {
            "table": table,
            "change_type": change_type,
            "affected_tables": tables,
            "affected_reports": reports,
            "total_impact": len(downstream),
            "criticality": "HIGH" if reports else "MEDIUM" if tables else "LOW",
        }

    def root_cause(self, table):
        upstream = self.tracker.lg.upstream(table)
        sources = [n for n in upstream
                   if self.tracker.lg.graph.nodes[n].get("node_type") == "source"]
        return {"table": table, "root_sources": sources}

from src.graph import LineageGraph

class LineageTracker:
    def __init__(self):
        self.lg = LineageGraph()

    def register_source(self, table, system):
        self.lg.add_node(table, node_type="source", system=system)

    def register_transformation(self, source_tables, target_table,
                                 job_name, transformation):
        self.lg.add_node(target_table, node_type="table")
        for src in source_tables:
            self.lg.add_edge(src, target_table,
                             transformation=transformation, job=job_name)

    def register_report(self, source_table, report_name):
        self.lg.add_node(report_name, node_type="report")
        self.lg.add_edge(source_table, report_name)

    def get_lineage(self, table):
        return {
            "table": table,
            "upstream": self.lg.upstream(table),
            "downstream": self.lg.downstream(table),
        }

    def full_graph(self):
        return self.lg.to_json()

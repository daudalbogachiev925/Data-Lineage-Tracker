from src.lineage import LineageTracker
from src.impact import ImpactAnalyzer

def test_upstream_downstream():
    t = LineageTracker()
    t.register_source("a", "sys")
    t.register_transformation(["a"], "b", "job1", "x")
    t.register_transformation(["b"], "c", "job2", "y")
    lineage = t.get_lineage("b")
    assert "a" in lineage["upstream"]
    assert "c" in lineage["downstream"]

def test_impact_analysis():
    t = LineageTracker()
    t.register_source("a", "sys")
    t.register_transformation(["a"], "b", "j", "x")
    t.register_report("b", "report1")
    impact = ImpactAnalyzer(t).impact_of_change("a")
    assert "report1" in impact["affected_reports"]
    assert impact["criticality"] == "HIGH"

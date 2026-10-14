import streamlit as st
import streamlit.components.v1 as components
from src.lineage import LineageTracker
from src.impact import ImpactAnalyzer
from src.viz import plot_lineage
from src.parser import parse_sql_lineage

st.set_page_config(page_title="Data Lineage", layout="wide")
st.title("🔗 Data Lineage Tracker")

tracker = LineageTracker()

# Seed
tracker.register_source("raw.customers", "PostgreSQL")
tracker.register_source("raw.orders", "PostgreSQL")
tracker.register_transformation(["raw.customers", "raw.orders"],
                                 "dwh.fact_sales", "etl_sales", "JOIN on customer_id")
tracker.register_transformation(["raw.customers"],
                                 "dwh.dim_customer", "etl_dim_customer", "SCD2")
tracker.register_transformation(["dwh.fact_sales", "dwh.dim_customer"],
                                 "mart.sales_report", "dbt_report", "AGG daily")
tracker.register_report("mart.sales_report", "dashboard.sales_executive")

tab1, tab2, tab3 = st.tabs(["📊 Граф", "🔎 Lineage", "💥 Impact Analysis"])

with tab1:
    fig = plot_lineage(tracker.lg.graph)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    table = st.selectbox("Таблица",
                          [n for n in tracker.lg.graph.nodes])
    st.json(tracker.get_lineage(table))

with tab3:
    table = st.selectbox("Impact для", [n for n in tracker.lg.graph.nodes], key="impact")
    if st.button("Анализировать"):
        st.json(ImpactAnalyzer(tracker).impact_of_change(table))

st.divider()
st.subheader("🧩 Парсер SQL")
sql = st.text_area("SQL:", "INSERT INTO dwh.fact_sales SELECT * FROM raw.orders JOIN raw.customers")
if st.button("Парсить"):
    st.json(parse_sql_lineage(sql))

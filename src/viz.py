import networkx as nx
import plotly.graph_objects as go

def plot_lineage(graph, title="Data Lineage"):
    pos = nx.spring_layout(graph, seed=42)
    edge_x, edge_y = [], []
    for u, v in graph.edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines",
                            line=dict(width=1, color="#888"))
    node_x, node_y, texts, colors = [], [], [], []
    color_map = {"source": "#1f77b4", "table": "#2ca02c", "report": "#ff7f0e"}
    for n in graph.nodes:
        x, y = pos[n]
        node_x.append(x); node_y.append(y)
        texts.append(n)
        colors.append(color_map.get(graph.nodes[n].get("node_type", "table"), "#999"))

    node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text",
                            text=texts, textposition="top center",
                            marker=dict(size=20, color=colors, line=dict(width=2)))
    return go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(title=title, showlegend=False,
                                      hovermode="closest"))

import sqlalchemy
import networkx as nx
import matplotlib.pyplot as plt

def connect_to_database(db_url):
    engine = sqlalchemy.create_engine(db_url)
    metadata = sqlalchemy.MetaData()
    metadata.reflect(bind=engine)
    return metadata

def build_knowledge_graph(metadata):
    G = nx.DiGraph()

    for table in metadata.tables.values():
        G.add_node(table.name, type="table")

        for column in table.columns:
            G.add_node(f"{table.name}.{column.name}", type="column")
            G.add_edge(table.name, f"{table.name}.{column.name}", relation="has_column")

    for table in metadata.tables.values():
        for column in table.columns:
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    referenced_table = fk.column.table.name
                    G.add_edge(table.name, referenced_table, relation="foreign_key")

    return G

def visualize_knowledge_graph(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)

    labels = {node: node for node in G.nodes()}

    table_nodes = [node for node, attr in G.nodes(data=True) if attr["type"] == "table"]
    column_nodes = [node for node, attr in G.nodes(data=True) if attr["type"] == "column"]

    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1500, font_size=8, edge_color="gray")
    nx.draw_networkx_nodes(G, pos, nodelist=table_nodes, node_color="lightblue", node_size=2000)
    nx.draw_networkx_nodes(G, pos, nodelist=column_nodes, node_color="lightgreen", node_size=1000)

    # **🔹 Fix: Draw Edge Labels (Show Relationships)**
    edge_labels = {(u, v): d["relation"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")

    plt.title("Knowledge Graph of Relational Database Schema")
    plt.show()

db_url = "mysql+pymysql://root:vedant3006@localhost/complex_db"
metadata = connect_to_database(db_url)
G = build_knowledge_graph(metadata)
visualize_knowledge_graph(G)

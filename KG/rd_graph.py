# kg_functions.py
import os
import sqlalchemy
import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, URIRef, Literal, RDF

def connect_to_database(db_url):
    engine = sqlalchemy.create_engine(db_url)
    metadata = sqlalchemy.MetaData()
    metadata.reflect(bind=engine)
    return metadata

def build_knowledge_graph(metadata):
    G = nx.DiGraph()
    # Add tables and their columns
    for table in metadata.tables.values():
        G.add_node(table.name, type="table")
        for column in table.columns:
            col_node = f"{table.name}.{column.name}"
            G.add_node(col_node, type="column")
            G.add_edge(table.name, col_node, relation="has_column")
    # Add foreign key relationships
    for table in metadata.tables.values():
        for column in table.columns:
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    referenced_table = fk.column.table.name
                    G.add_edge(table.name, referenced_table, relation="foreign_key")
    return G

def convert_graph_to_rdf(G):
    rdf_graph = Graph()
    base_uri = "http://example.org/"
    
    # Create RDF resources for tables and columns
    for node, attr in G.nodes(data=True):
        if attr.get("type") == "table":
            table_uri = URIRef(base_uri + node)
            rdf_graph.add((table_uri, RDF.type, URIRef(base_uri + "Table")))
            rdf_graph.add((table_uri, URIRef(base_uri + "has_name"), Literal(node)))
        elif attr.get("type") == "column":
            column_uri = URIRef(base_uri + node)
            rdf_graph.add((column_uri, RDF.type, URIRef(base_uri + "Column")))
            rdf_graph.add((column_uri, URIRef(base_uri + "has_name"), Literal(node.split('.')[-1])))
    
    # Add relationships as RDF triples
    for u, v, data in G.edges(data=True):
        subject_uri = URIRef(base_uri + u)
        object_uri = URIRef(base_uri + v)
        relation = URIRef(base_uri + data['relation'])
        rdf_graph.add((subject_uri, relation, object_uri))
    
    return rdf_graph

def save_rdf_to_file(rdf_graph, filename="knowledge_graph.rdf"):
    rdf_graph.serialize(destination=filename, format="turtle")

def visualize_knowledge_graph(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    labels = {node: node for node in G.nodes()}
    
    table_nodes = [node for node, attr in G.nodes(data=True) if attr.get("type") == "table"]
    column_nodes = [node for node, attr in G.nodes(data=True) if attr.get("type") == "column"]
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1500, font_size=8, edge_color="gray")
    nx.draw_networkx_nodes(G, pos, nodelist=table_nodes, node_color="lightblue", node_size=2000)
    nx.draw_networkx_nodes(G, pos, nodelist=column_nodes, node_color="lightgreen", node_size=1000)
    
    edge_labels = {(u, v): d["relation"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")
    
    plt.title("Knowledge Graph of Relational Database Schema")
    plt.show()

def generate_rdf_template_from_kg(G, base_uri="http://example.org/"):
    """
    Generate an RDF template (in Turtle syntax) from the KG.
    Placeholders (within {}) are inserted for later mapping via the LLM.
    """
    template = "@prefix ex: <{base_uri}> .\n\n".format(base_uri=base_uri)
    
    # Process table nodes
    for node, attr in G.nodes(data=True):
        if attr.get("type") == "table":
            template += f"### Entity: {node}\n"
            template += f"ex:{node} a ex:Table ;\n"
            template += f'    ex:has_name "{{{node}_has_name}}" ;\n'
            
            columns = []
            for neighbor in G.successors(node):
                neighbor_attr = G.nodes.get(neighbor, {})
                if neighbor_attr.get("type") == "column" and neighbor.startswith(f"{node}."):
                    col = neighbor.split('.')[-1]
                    columns.append(f"ex:{node}_{col}")
            if columns:
                template += "    ex:has_columns " + ", ".join(columns) + " ;\n"
            template = template.rstrip(" ;\n") + " .\n\n"
    
    # Process column nodes
    for node, attr in G.nodes(data=True):
        if attr.get("type") == "column":
            try:
                table, col = node.split('.', 1)
            except ValueError:
                continue
            template += f"ex:{table}_{col} a ex:Column ;\n"
            template += f'    ex:has_name "{{{table}_{col}_has_name}}" .\n\n'
    
    # Add foreign key relationships
    for u, v, data in G.edges(data=True):
        if data.get("relation") == "foreign_key":
            template += f"ex:{u} ex:foreign_key ex:{v} .\n"
    
    return template

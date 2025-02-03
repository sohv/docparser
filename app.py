import os
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from rdflib import Graph
from KG.rd_graph import (
    connect_to_database,
    build_knowledge_graph,
    generate_rdf_template_from_kg,
    visualize_knowledge_graph,
    save_rdf_to_file
)
from LLM.llm_mapper import map_to_kg_template 
from LLM.preprocess import preprocess_text
import networkx as nx
import matplotlib.pyplot as plt

load_dotenv()


def plot_rdf_graph(rdf_graph):
    nx_graph = nx.Graph()
    for subj, pred, obj in rdf_graph:
        print(subj, pred, obj)  
        subj_str = str(subj)
        pred_str = str(pred)
        obj_str = str(obj)
        nx_graph.add_edge(subj_str, obj_str, label=pred_str)
    pos = nx.spring_layout(nx_graph, k=0.8, seed=42)  
    plt.figure(figsize=(50,50 ))  
    nx.draw(
        nx_graph, pos, with_labels=True, node_size=1000, 
        node_color="lightblue", font_size=7, font_weight="bold", edge_color="gray"
    )
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    nx.draw_networkx_edge_labels(
        nx_graph, pos, edge_labels=edge_labels, font_size=7, font_color="red", rotate=True
    )
    plt.title("RDF Graph Visualization", fontsize=10, fontweight="bold")
    plt.show()


def main():
    db_url = "mysql+pymysql://root:password@localhost/complex_db"
    metadata = connect_to_database(db_url)
    if not metadata:
        print("Failed to connect to database")
        return
    G = build_knowledge_graph(metadata)  
    if not G:
        print("Failed to build knowledge graph")
        return
    rdf_template = generate_rdf_template_from_kg(G)
    raw_text = (
            """John is an enthusiastic member of our e-commerce platform.
            He joined in March 2021 and has made several purchases over the years.
            Recently, he bought a smartphone and left a detailed review describing his experience with the product.
            His review received multiple upvotes and sparked a discussion among other customers.
            John also added a new payment method to his account and updated his shipping address.
            Additionally, he recommended a laptop to a friend through the referral program.
            Later in the day, he browsed through the latest offers and added a smartwatch to his wishlist."""
    )
    text = preprocess_text(raw_text) 
    kg_structured_output = map_to_kg_template(text, rdf_template)
    print("Structured KG Output:", kg_structured_output)  
    kg_structured_output = kg_structured_output.split("Note:")[0]   
    rdf_template_with_prefix = """
    @prefix ex: <http://example.org/> . 
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . 
    """ + kg_structured_output  

    rdf_graph = Graph()   
    try:
        rdf_graph.parse(data=rdf_template_with_prefix, format="ttl")
    except Exception as e:
        print("Error parsing RDF data:", e)
        return
    
    plot_rdf_graph(rdf_graph)
if __name__ == "__main__":
    main()


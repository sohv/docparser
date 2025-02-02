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

load_dotenv()

def plot_rdf_graph(rdf_graph):
    nx_graph = nx.Graph()
    
    # Print RDF triples to debug
    for subj, pred, obj in rdf_graph:
        print(subj, pred, obj)  # Debugging line to print the RDF triples
        subj_str = str(subj)
        pred_str = str(pred)
        obj_str = str(obj)
        nx_graph.add_edge(subj_str, obj_str, label=pred_str)
    
    # Layout for more spacious plotting
    pos = nx.spring_layout(nx_graph, k=0.3, seed=42)  # Adjust k for better spacing
    nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)
    plt.title("RDF Graph Visualization")
    plt.show()

def main():
    db_url = "mysql+pymysql://root:password@localhost/complex_db"
    
    # Check if connection is successful
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
        "Alice is an active user on our social media platform. "
        "She registered on the platform in January 2022 and has been very active ever since. "
        "Alice recently created a new post about her trip to the mountains, sharing several photos and a detailed description of her experience. "
        "Her post received many likes and comments. "
        "Alice also commented on a friend's post about a local event, expressing her excitement and asking for more details. "
        "Later that day, she liked another post by one of her connections, showing her appreciation for the shared content. "
        "In addition to these activities, Alice updated her profile information and added new interests."
    )

    text = preprocess_text(raw_text)
    
    # Map to RDF template and print output for debugging
    kg_structured_output = map_to_kg_template(text, rdf_template)
    print("Structured KG Output:", kg_structured_output)  # Debugging line
    
    # Remove any non-RDF information like the 'Note:' section
    kg_structured_output = kg_structured_output.split("Note:")[0]  # Split and keep only the valid RDF part
    
    rdf_template_with_prefix = """
    @prefix ex: <http://example.org/> . 
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . 
    """ + kg_structured_output  # Add the cleaned RDF output
    
    rdf_graph = Graph()   
    try:
        rdf_graph.parse(data=rdf_template_with_prefix, format="ttl")
    except Exception as e:
        print("Error parsing RDF data:", e)
        return
    
    # Visualize the RDF graph
    plot_rdf_graph(rdf_graph)

if __name__ == "__main__":
    main()


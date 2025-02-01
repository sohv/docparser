# integration.py
import os
from dotenv import load_dotenv
from KG.rd_graph import (
    connect_to_database,
    build_knowledge_graph,
    convert_graph_to_rdf,
    generate_rdf_template_from_kg,
    visualize_knowledge_graph,
    save_rdf_to_file
)
from LLM.llm_mapper import map_to_kg_template

# Load environment variables (ensure GROQ_API_KEY is set in your .env file)
load_dotenv()

def main():
    # --- Database Connection & KG Building ---
    db_url = "mysql+pymysql://root:password@localhost/complex_db"
    metadata = connect_to_database(db_url)
    G = build_knowledge_graph(metadata)
    
    # Optionally visualize the Knowledge Graph
    #visualize_knowledge_graph(G)
    
    # Optionally convert the KG to RDF and save it to a file
    #rdf_graph = convert_graph_to_rdf(G)
    #save_rdf_to_file(rdf_graph, filename="knowledge_graph.rdf")
    
    # --- Generate the RDF Template from the KG ---
    rdf_template = generate_rdf_template_from_kg(G)
    #print("Generated RDF Template:\n")
    #print(rdf_template)
    
    # --- Define Raw Text for Mapping ---
    # This raw text explains a user and their activity on the social media platform.
    raw_text = (
        "Alice is an active user on our social media platform. "
        "She registered on the platform in January 2022 and has been very active ever since. "
        "Alice recently created a new post about her trip to the mountains, sharing several photos and a detailed description of her experience. "
        "Her post received many likes and comments. "
        "Alice also commented on a friend's post about a local event, expressing her excitement and asking for more details. "
        "Later that day, she liked another post by one of her connections, showing her appreciation for the shared content. "
        "In addition to these activities, Alice updated her profile information and added new interests."
    )
    
    # --- Map the Raw Text to the RDF Template using the Groq LLM ---
    kg_structured_output = map_to_kg_template(raw_text, rdf_template)
    print("\nStructured KG Output from LLM:\n")
    print(kg_structured_output)

if __name__ == "__main__":
    main()

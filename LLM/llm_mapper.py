import os
from groq import Groq
from urllib.parse import urlparse
from sqlalchemy import create_engine, MetaData, Table


def get_all_tables_from_db():
    """
    Reflect all tables in the database dynamically using SQLAlchemy.
    """
    db_url = "mysql+pymysql://root:vedant3006@localhost/complex_db"

 
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables = metadata.tables
    print("Tables in the database:", tables.keys())

    for table_name, table in tables.items():
        print(f"Table: {table_name}")
        for column in table.columns:
            print(f"  Column: {column.name}, Type: {column.type}")

    return tables

def map_to_kg_template(raw_text, kg_template, model="llama-3.3-70b-versatile", temperature=0.1, max_tokens=1024):
    """
    Maps raw text to a structured KG template using the Groq LLM.
    
    Parameters:
      - raw_text (str): The unstructured input text.
      - kg_template (str): The predefined KG template to structure the data.
      - model (str): The LLM model to use.
      - temperature (float): Controls randomness (lower values for more deterministic output).
      - max_tokens (int): Maximum number of tokens in the response.
      
    Returns:
      - str: The structured KG representation.
    """
    last_primary_key = get_all_tables_from_db()

    dynamic_info = f"The last primary key value in the database is {last_primary_key}."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
You are an AI system that converts raw text into a structured Knowledge Graph (KG) format.

- Input Raw Text:
{raw_text}

- Given KG Template (covering the entire database schema):
{kg_template}

- Task:
Analyze the input text and map only the relevant information to the corresponding parts of the KG template. 
You do not need to fill in the entire template; only populate the sections that match the content in the raw text.
Ensure that the entity relationships are correctly identified and mapped to the most suitable parts of the template.

- Database Context:
{dynamic_info}

- Output:
Return only the structured KG representation.
"""

    chat_completion = client.chat.completions.create(
        messages=[ 
            {"role": "system", "content": "You are a structured data mapper for Knowledge Graphs."},
            {"role": "user", "content": prompt}
        ],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        stop=None,
        stream=False,
    )
    
    return chat_completion.choices[0].message.content

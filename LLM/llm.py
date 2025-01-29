from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()


def map_to_kg_template(raw_text, kg_template, model="llama-3.3-70b-versatile", temperature=0.1, max_tokens=1024):
    """
    Maps raw text to a structured Knowledge Graph (KG) template using an LLM.

    Parameters:
    - raw_text (str): The unstructured input text.
    - kg_template (str): The predefined KG template to structure the data.
    - model (str): The LLM model to use (default: "llama-3.3-70b-versatile").
    - temperature (float): Controls randomness (default: 0.1 for structured output).
    - max_tokens (int): Maximum response tokens (default: 1024).

    Returns:
    - str: The structured KG representation.
    """
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    You are an AI system that converts raw text into a structured Knowledge Graph (KG) format.

    - Input Raw Text:
    {raw_text}

    - Given KG Template:
    {kg_template}

    - Task:
    Map the input text to match the provided KG template strictly, ensuring correct entity relationships.
    
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


raw_text = "Elon Musk founded Tesla and SpaceX."
kg_template = """
<Entity: Person>
    Name: {Person_Name}
    Organizations: {Organizations_Founded}
</Entity>

<Entity: Organization>
    Name: {Organization_Name}
    Founder: {Founder_Name}
</Entity>
"""
kg_output = map_to_kg_template(raw_text, kg_template)
print(kg_output)

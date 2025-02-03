import re
import nltk
import spacy
import contractions
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

# Custom Stopwords
custom_stopwords = set(["please", "use", "like", "also", "would", "could"])
stop_words = set(stopwords.words('english')).union(custom_stopwords)

def handle_negations(tokens):
    """Combines negation words with the following word for better meaning retention."""
    processed_tokens = []
    skip = False
    for i, word in enumerate(tokens):
        if word == "not" and i + 1 < len(tokens):
            processed_tokens.append(f"{word}_{tokens[i+1]}")  # Combine "not" with next word
            skip = True
        elif skip:
            skip = False
        else:
            processed_tokens.append(word)
    return processed_tokens

def get_synonym(word):
    """Finds the first synonym for a given word using WordNet."""
    synonyms = wordnet.synsets(word)
    return synonyms[0].lemmas()[0].name() if synonyms else word

def extract_named_entities(text):
    """Extracts Named Entities (e.g., names, dates, locations) from text using spaCy."""
    doc = nlp(text)
    return [ent.text for ent in doc.ents]  # Example: ["Alice", "2022"]

def preprocess_text(text):
    """Applies text normalization, tokenization, lemmatization, stopword removal, and NER filtering."""
    # Normalize text
    text = contractions.fix(text)  # Expand contractions
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip().lower()  # Remove extra spaces

    # Named Entity Extraction (Preserving important entities)
    named_entities = extract_named_entities(text)

    sentences = sent_tokenize(text)
    processed_sentences = []
    lemmatizer = WordNetLemmatizer()

    for sentence in sentences:
        tokens = word_tokenize(sentence)

        # Handle negations
        tokens = handle_negations(tokens)

        # Remove stopwords while preserving named entities
        tokens = [word for word in tokens if word in named_entities or word not in stop_words]

        # Lemmatization & Synonym Normalization
        tokens = [get_synonym(lemmatizer.lemmatize(word)) for word in tokens]

        # POS Filtering (Remove adjectives and adverbs)
        tokens = [word for word, tag in pos_tag(tokens) if tag not in ["JJ", "RB"]]

        processed_sentences.append(" ".join(tokens))

    return processed_sentences


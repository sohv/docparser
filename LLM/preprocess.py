import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    sentences = sent_tokenize(text)

    processed_sentences = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        processed_sentences.append(' '.join(tokens))
    return processed_sentences

# Given text
# text = """Each project manual is a large volume of unstructured texts containing task descriptions and complex instructions.
# It was overwhelming for a domain expert to go through the course material and to identify key entities and relations.
# So we used the bottom-up approach by applying natural-language-processing-based named-entity recognition (NER) methods 
# to extract raw entities and relations. The NER method relies on parts of speech (POS) tagging, which extracts the subject 
# and object as entities and the verb or the root of a sentence as a relation. We performed the following steps for 
# preprocessing the text and building the preliminary visual representation of data."""

# # Apply preprocessing
# processed_text = preprocess_text(text)

# # Print results
# for sent in processed_text:
#     print(sent)

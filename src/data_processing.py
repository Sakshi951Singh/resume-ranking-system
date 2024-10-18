import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch

# Load SpaCy model and BERT model and tokenizer
nlp = spacy.load("en_core_web_sm")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Function to extract skills (considering that your NER model might need custom training)
def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return skills

# Function to preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())
    # Keeping lemmatization and removing stop words
    processed = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return processed

# Function to get embeddings using BERT
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Mean pooling of BERT output for embeddings
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Function to rank resumes based on JD
def rank_resumes(resume_text, jd_text):
    # Preprocess texts
    resume_text = preprocess_text(resume_text)
    jd_text = preprocess_text(jd_text)

    # Get BERT embeddings
    resume_embedding = get_bert_embeddings(resume_text)
    jd_embedding = get_bert_embeddings(jd_text)

    # Calculate cosine similarity
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    
    return score

# Example Usage
if __name__ == "__main__":
    # Sample resume and job description texts
    resume_sample = "Software engineer with experience in Python, Java,HTML,CSS and machine learning."
    jd_sample = "Looking for a software engineer with strong skills in HTML,CSS Python and machine learning."

    score = rank_resumes(resume_sample, jd_sample)
    print(f"Resume Score: {score:.2f}")

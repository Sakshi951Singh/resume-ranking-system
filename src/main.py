# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def rank_resumes(resume_path, jd_path):
#     resume_text = read_file_as_text(resume_path)
#     jd_text = read_file_as_text(jd_path)
    
#     # Vectorize the texts
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform([resume_text, jd_text])
    
#     # Calculate cosine similarity
#     score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
#     return score

# def read_file_as_text(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as f:
#             return f.read()




# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Function to rank multiple resumes against a job description
# def rank_multiple_resumes(resume_paths, jd_path):
#     jd_text = read_file_as_text(jd_path)

#     # List to store (resume_filename, score) tuples
#     results = []

#     for resume_path in resume_paths:
#         resume_text = read_file_as_text(resume_path)
        
#         # Ensure both texts are not empty
#         if not resume_text or not jd_text:
#             raise ValueError(f"Resume or Job Description is empty: {resume_path}")
        
#         # Vectorize the texts
#         vectorizer = TfidfVectorizer()
#         vectors = vectorizer.fit_transform([resume_text, jd_text])

#         # Calculate cosine similarity
#         score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
#         # Store result as a tuple (resume_filename, score)
#         results.append((os.path.basename(resume_path), score))
    
#     # Sort results by score in descending order
#     results.sort(key=lambda x: x[1], reverse=True)
    
#     return results

# # Function to read the file content as text
# def read_file_as_text(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as f:
#             return f.read()





# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from src.main import rank_multiple_resumes  # Ensure this import works based on your project structure


# def read_file_as_text(file_path):
#     """
#     Reads a file and returns its content as a string.
#     Handles potential encoding issues by trying utf-8 first, then latin-1.
#     """
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as f:
#             return f.read()

# def rank_resumes(resume_text, jd_text):
#     """
#     Rank a single resume against the job description using TF-IDF and cosine similarity.
#     """
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform([resume_text, jd_text])
    
#     # Calculate cosine similarity
#     score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
#     return score

# def rank_multiple_resumes(resume_paths, jd_path):
#     """
#     Rank multiple resumes against a job description.
#     """
#     jd_text = read_file_as_text(jd_path)
#     scores = []
    
#     for resume_path in resume_paths:
#         resume_text = read_file_as_text(resume_path)
#         score = rank_resumes(resume_text, jd_text)
#         resume_filename = os.path.basename(resume_path)
#         scores.append((resume_filename, round(score * 100, 1)))  # Convert score to percentage
    
#     return scores







import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_file_as_text(file_path):
    """
    Reads a file and returns its content as a string.
    Handles potential encoding issues by trying utf-8 first, then latin-1.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()

def rank_resumes(resume_text, jd_text):
    """
    Rank a single resume against the job description using TF-IDF and cosine similarity.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    
    # Calculate cosine similarity
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return score

def rank_multiple_resumes(resume_paths, jd_path):
    """
    Rank multiple resumes against a job description.
    """
    jd_text = read_file_as_text(jd_path)
    scores = []
    
    for resume_path in resume_paths:
        resume_text = read_file_as_text(resume_path)
        score = rank_resumes(resume_text, jd_text)
        resume_filename = os.path.basename(resume_path)
        scores.append((resume_filename, round(score * 100, 1)))  # Convert score to percentage
    
    return scores








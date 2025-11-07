from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resume(resume_text: str, job_text: str) -> float:
    """Return similarity score between resume and job description (0–100)."""
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(similarity * 100, 2)

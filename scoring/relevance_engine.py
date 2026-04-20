from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_relevance(experiences, job_text):
    if not experiences:
        return experiences, 0

    vectorizer = TfidfVectorizer()

    texts = [job_text] + [exp["role"] for exp in experiences]
    vectors = vectorizer.fit_transform(texts)

    jd_vector = vectors[0]

    scores = []
    for i, exp in enumerate(experiences):
        role_vector = vectors[i+1]
        score = cosine_similarity(jd_vector, role_vector)[0][0]

        exp["relevance_score"] = round(float(score), 2)
        scores.append(score)

    overall = sum(scores) / len(scores)
    return experiences, round(overall, 2)
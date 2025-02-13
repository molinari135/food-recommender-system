import re

def parse_markdown(filename=r"C:\Users\Ester\Documents\SIIA\food-recommender-system\data\raw\nutritional-infos.md"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex to match headers (## ) and their content until the next header
    pattern = r"## (.+?)\n(.*?)(?=\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Store each question-answer pair
    chunks = [{"header": q.strip(), "content": a.strip()} for q, a in matches]
    
    return chunks

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_most_relevant_question(query, chunks):
    # Extract headers (questions)
    headers = [chunk["header"] for chunk in chunks]
    
    # Vectorize using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(headers + [query])  # Include query
    
    # Compute similarity between query and headers
    similarity = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    
    # Get the most similar header
    best_match_idx = similarity.argmax()
    return chunks[best_match_idx]  # Return the best-matching chunk

chunks = parse_markdown()
query = "Why saturated fat are bad?"
best_match = find_most_relevant_question(query, chunks)

print("Query:", query)
print("Best Match:", best_match["header"])
print("Answer:", best_match["content"])

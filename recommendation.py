import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import re

# Load data with embeddings
df = pd.read_pickle("f:/Project/SHL/assessments_with_embeddings.pkl")
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_assessments(query, max_duration=None, top_k=10):
    # Extract duration constraint from query (e.g., "less than 40 minutes")
    duration_match = re.search(r'less than (\d+) minutes', query, re.IGNORECASE)
    if duration_match:
        max_duration = int(duration_match.group(1))
    elif max_duration is None:
        max_duration = float('inf')  # No limit if unspecified

    # Keyword matching
    keywords = query.lower().split()
    df['keyword_score'] = df['combined_text'].apply(
        lambda x: sum(1 for word in keywords if word in x.lower())
    )

    # Semantic search
    query_embedding = model.encode(query)
    embeddings = np.stack(df['embedding'].values)
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    df['semantic_score'] = cosine_scores

    # Combine scores (adjust weights as needed)
    df['total_score'] = 0.4 * df['keyword_score'] + 0.6 * df['semantic_score']

    # Filter by duration (handle non-numeric values)
    df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce').fillna(float('inf'))
    filtered_df = df[df['Duration'] <= max_duration]

    # Sort and return top results
    top_results = filtered_df.sort_values('total_score', ascending=False).head(top_k)
    return top_results[['Assessment Name', 'Duration', 'Test Type', 'total_score']]

# Test the function
if __name__ == "__main__":
    sample_query = "assessments for software engineer less than 40 minutes"
    results = recommend_assessments(sample_query)
    print("Recommendations for:", sample_query)
    print(results.to_string(index=False))
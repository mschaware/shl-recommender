import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import re

# Use relative path for local and Render compatibility
df = pd.read_pickle("assessments_with_embeddings.pkl")
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_assessments(query, max_duration=None, top_k=10):
    duration_match = re.search(r'less than (\d+) minutes', query, re.IGNORECASE)
    if duration_match:
        max_duration = int(duration_match.group(1))
    elif max_duration is None:
        max_duration = float('inf')

    keywords = query.lower().split()
    df['keyword_score'] = df['combined_text'].apply(
        lambda x: sum(1 for word in keywords if word in x.lower())
    )

    query_embedding = model.encode(query)
    embeddings = np.stack(df['embedding'].values)
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    df['semantic_score'] = cosine_scores

    df['total_score'] = 0.4 * df['keyword_score'] + 0.6 * df['semantic_score']

    df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce').fillna(float('inf'))
    filtered_df = df[df['Duration'] <= max_duration]

    top_results = filtered_df.sort_values('total_score', ascending=False).head(top_k)
    return_columns = ['Assessment Name', 'URL', 'Remote Testing Support', 'Adaptive/IRT Support', 'Duration', 'Test Type', 'total_score']
    return top_results[return_columns]
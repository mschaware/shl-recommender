import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load preprocessed data
df = pd.read_csv("f:/Project/SHL/shl_assessments_preprocessed.csv")

# Fill missing values for text columns
text_columns = ['Assessment Name', 'Test Type']  # Adjust based on your columns
for col in text_columns:
    df[col] = df[col].fillna('')

# Combine text fields for embedding
df['combined_text'] = df['Assessment Name'] + ' ' + df['Test Type']

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
df['embedding'] = list(embeddings)

# Save for later use
df.to_pickle("f:/Project/SHL/assessments_with_embeddings.pkl")
print("Data with embeddings saved to assessments_with_embeddings.pkl")
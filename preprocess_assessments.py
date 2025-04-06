import pandas as pd
import re

# Load the original CSV
df = pd.read_csv("f:/Project/SHL/shl_assessments.csv")

# Extract numeric duration from 'Duration' column
df['Duration'] = df['Duration'].str.extract(r'(\d+)').fillna('')

# Save to preprocessed CSV with a different name
df.to_csv("f:/Project/SHL/shl_assessments_preprocessed_new.csv", index=False)

print("Preprocessed data saved to shl_assessments_preprocessed_new.csv")
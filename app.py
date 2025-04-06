import streamlit as st
from recommendation import recommend_assessments

st.title("SHL Assessment Recommender")

# User input
query = st.text_input("Enter your query (e.g., 'assessments for software engineer less than 40 minutes')", "")

if query:
    # Get recommendations
    results = recommend_assessments(query)
    
    # Display results
    st.write("Top Recommendations:")
    st.dataframe(results)
    
    # JSON output for API-like response
    st.write("JSON Output:")
    st.json(results.to_dict(orient='records'))

# Run: streamlit run app.py
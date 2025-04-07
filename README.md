# SHL Assessment Recommender 🚀

Welcome to the **SHL Assessment Recommender**—a slick, AI-powered web tool that turns hiring headaches into a breeze! Built with ❤️ and grit, this app takes natural language queries (think "Java devs under 40 mins") and dishes out the top SHL assessments from their catalog, served up in a neat table and JSON via a snappy API. Buckle up for the ride—we’re spilling the whole story of how we made this magic happen! 🎉

## 🎥 See It in Action!
Check out our demo on YouTube:  
[![SHL Assessment Recommender Demo](https://img.youtube.com/vi/zM6sUHW2d0Y/0.jpg)](https://youtu.be/zM6sUHW2d0Y)

## 🌟 What’s the Big Deal?
Hiring managers deserve better than clunky keyword searches. We crafted a system that:
- **Listens**: Takes your job queries or descriptions like a pro.
- **Recommends**: Delivers up to 10 spot-on SHL assessments with all the juicy details:
  - Assessment Name & URL 📎
  - Remote Testing Support (Yes/No) ✅
  - Adaptive/IRT Support (Yes/No) ⚙️
  - Duration ⏱️ & Test Type 🧪
- **Shines**: Offers a Streamlit UI and a Flask API for ultimate flexibility.

## 🛠️ The Epic Journey: How We Built It

### Step 1: Hunting the Data 🕵️‍♂️
We kicked off by raiding the [SHL Product Catalog](https://www.shl.com/solutions/products/product-catalog/). Armed with `selenium` and `chromedriver`, we scraped the goods into `shl_assessments.csv`. Then, we polished it up with `preprocess_assessments.py`, creating `shl_assessments_preprocessed.csv`—our golden dataset.

### Step 2: Brainpower Unleashed 🤖
Using `sentence-transformers` (`all-MiniLM-L6-v2`), we turned text into embeddings, stored in `assessments_with_embeddings.pkl`. Our secret sauce? A hybrid scoring system in `recommendation.py`:
- 40% keyword magic ✨
- 60% semantic smarts 🧠
- Filtered by duration with regex wizardry 🔍

### Step 3: Building the Beast 🏗️
- **Streamlit UI (`app.py`)**: A sleek interface for query fun, spitting out tables and JSON.
- **Flask API (`server.py`)**: A GET endpoint (`/api/recommend`) for JSON on demand.
- **Deployment Drama**: Vercel’s 250 MB limit crushed us, so we pivoted to Render. Fought path errors, version clashes, and Hugging Face rate limits—bundled the model in `model_cache` to win!

## 🚀 Live and Kicking
- **Demo URL**: [https://shl-recommender-w2q9.onrender.com/](https://shl-recommender-w2q9.onrender.com/)
- **API Endpoint**: [https://shl-recommender-w2q9.onrender.com/api/recommend](https://shl-recommender-w2q9.onrender.com/api/recommend)
- **GitHub**: [https://github.com/mschaware/shl-recommender](https://github.com/mschaware/shl-recommender)

## 🧑‍💻 Setup: Be a Hero Locally
1. **Grab the Code**:
   ```bash
   git clone https://github.com/mschaware/shl-recommender.git
   cd shl-recommender

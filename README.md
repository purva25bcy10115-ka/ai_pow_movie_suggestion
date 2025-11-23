# 🎬 Movie Recommendation Engine (with Local LLM Support)

This project is a content-based movie recommendation system that suggests similar movies using text-based feature engineering, cosine similarity, and optional enhancements using local LLMs (Ollama).

It works fully offline once your dataset and models are downloaded.

## 📌 Features
✅ 1. Movie Recommendation System

Uses CountVectorizer to convert movie tags into numerical vectors

Computes cosine similarity between movies

Recommends Top 10 similar movies

✅ 2. Smart Movie Search

Handles user typos (spaiderman → Spider-Man)

Fuzzy matching with fuzzywuzzy

Optional local LLM enhancement for query expansion

✅ 3. Local LLM Integration (Optional)

Works with Ollama models

Currently uses Mistral or Llama3.2

Expands movie names dynamically

Can generate custom LLM messages if desired

## 🗂 Project Structure
ProjectAI/

│

├── recommendation_engine.py

├── llm_helper.py

├── movies_cleaned.csv

├── similarity.pkl  (auto-generated)

├── README.md

└── .venv/           (virtual environment)

 ## 🛠 Installation & Setup
1. Clone your GitHub repository (manual upload also works)
   ```bash
   git clone <your_repo_url>
   cd ProjectAI
   ```
   
2. Create & activate virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   ```

3. Install required Python packages
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Required Libraries

Here is the requirements.txt content
```bash
pandas
scikit-learn
fuzzywuzzy[speedup]
numpy
```

(LLM libraries like Ollama are optional, not needed for basic recommendations.)

## ⚙️ Running the Program
```bash
python recommendation_engine.py
```
You will be asked:
```bash
Enter movie name:
```
Example:
```bash
Enter movie name: iron man
```
The system prints:

LLM-expanded suggestions (if enabled)

Best fuzzy match

Top 10 recommended movies

## 🤖 Local LLM Integration (Optional)

Make sure Ollama is installed before enabling LLM features:

Install Ollama:

https://ollama.ai/download

Pull a model:
```bash
ollama pull mistral
```
The system uses:

mistral:latest by default

If the LLM fails or times out, the system falls back to fuzzy search.

## 📊 Dataset Used

movies_cleaned.csv
Contains columns:

title

tags

This is the main data file.
No credits file is used.

## 🧠 How Recommendation Works

**1.Combine movie metadata → create a tags column.**

**2.Convert tags to vectors with CountVectorizer.**

**3.Calculate cosine similarity between vectors.**

**4.For a given movie, pick highest similarity scores.**

**5.Display top recommendations.**


## 📝 Author

### Purva Kataria
Movie Recommendation Engine Project

**Python | Machine Learning | Local LLMs**

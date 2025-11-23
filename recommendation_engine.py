import sys
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import pickle
import subprocess
import json

# -------------------------------
# LLM Helper
# -------------------------------
def expand_query(movie_name):
    """
    Use LLM to get dynamic recommendation description.
    Returns a string describing the movie and similar suggestions.
    """
    prompt = f"""
    You are a movie recommendation assistant.
    User typed: "{movie_name}"
    Provide a short dynamic recommendation for this movie:
    - Include a few similar movie titles in the text.
    - Write naturally, like a friend suggesting a movie.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:latest"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore",
            timeout=120
        )
        output = result.stdout.strip()
        if output:
            return output
        else:
            return f"Recommended movies similar to '{movie_name}'."
    except Exception as e:
        print("❌ LLM Error:", e)
        return f"Recommended movies similar to '{movie_name}'."

# -------------------------------
# Dataset & Similarity
# -------------------------------
DATA_FILE = "movies_cleaned.csv"
SIM_FILE = "similarity.pkl"

if not os.path.exists(DATA_FILE):
    print(f"❌ Dataset file '{DATA_FILE}' not found")
    sys.exit(1)

print("Loading dataset...")
df = pd.read_csv(DATA_FILE, encoding='utf-8')

if "tags" not in df.columns:
    print("❌ Dataset must contain 'tags'")
    sys.exit(1)

if os.path.exists(SIM_FILE):
    print("Loading precomputed similarity matrix...")
    similarity = pickle.load(open(SIM_FILE, "rb"))
else:
    print("Vectorizing tags...")
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vector = cv.fit_transform(df["tags"].astype(str))
    print("Calculating similarity matrix...")
    similarity = cosine_similarity(vector)
    pickle.dump(similarity, open(SIM_FILE, "wb"))

# -------------------------------
# Smart Search (fuzzy matching)
# -------------------------------
def smart_find_movie(user_input):
    all_titles = df["title"].tolist()
    match = process.extractOne(user_input, all_titles)
    if match and match[1] > 50:  # threshold
        return match[0]
    return None

# -------------------------------
# Recommendation
# -------------------------------
def recommend(movie_title):
    if movie_title not in df["title"].values:
        print("❌ Movie not in database")
        return

    idx = df[df["title"] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)

    print("\nRecommended Movies:")
    for m in distances[1:11]:
        print("➡", df.iloc[m[0]].title)

# -------------------------------
# Main Program
# -------------------------------
if __name__ == "__main__":
    user_movie = input("Enter movie name: ").strip()

    best_match = smart_find_movie(user_movie)

    if best_match is None:
        print("❌ Could not identify the movie. Try again.")
    else:
        print(f"🎯 Best match found: {best_match}")
        # LLM dynamic reply
        dynamic_text = expand_query(best_match)
        print("\n💬 LLM says:")
        print(dynamic_text)
        # Regular recommendations
        recommend(best_match)

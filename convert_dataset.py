import pandas as pd
import ast

# Load datasets
print("Loading datasets...")
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets
print("Merging...")
movies = movies.merge(credits, on="title")

# Function to convert stringified list to normal list
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L

# Extract required fields
print("Extracting fields...")
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(lambda x: convert(x)[:3])
movies["crew"] = movies["crew"].apply(lambda x: [i["name"] for i in ast.literal_eval(x) if i["job"] == "Director"])

# Create tags column
print("Creating tags...")
movies["tags"] = movies["overview"].fillna("") + " " + \
                 movies["genres"].apply(lambda x: " ".join(x)) + " " + \
                 movies["keywords"].apply(lambda x: " ".join(x)) + " " + \
                 movies["cast"].apply(lambda x: " ".join(x)) + " " + \
                 movies["crew"].apply(lambda x: " ".join(x))

# Clean final dataset
print("Cleaning dataset...")
final_df = movies[["movie_id", "title", "tags"]]
final_df.to_csv("movies_cleaned.csv", index=False)

print("File generated: movies_cleaned.csv")

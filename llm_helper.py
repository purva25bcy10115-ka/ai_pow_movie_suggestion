import subprocess
import ast

def expand_query(movie_name):
    """
    Uses local Mistral model to expand the movie search query.
    Returns 5 alternative spellings, nicknames, or related titles.
    """
    prompt = f"""
    You are a movie keyword expander. 
    User typed: "{movie_name}"
    Return 5 alternative spellings, nicknames, or related titles as a Python list.
    """

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:latest"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore"
        )

        output = result.stdout.strip()

        # Try to parse as a Python literal
        try:
            return ast.literal_eval(output)
        except Exception:
            # fallback: split by commas and strip
            return [x.strip() for x in output.strip("[]").split(",") if x.strip()]

    except Exception as e:
        print("❌ LLM Error:", e)
        return [movie_name]

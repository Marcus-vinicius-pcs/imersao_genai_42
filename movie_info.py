import os
import json
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

def format_prompt(movie_title: str) -> str:
    return f"""
    <context>You are an assistant with the task of <task>returning information about a movie by movie title</task>.</context>
    <instruction>Provide information about the movie "{movie_title}" in JSON format with the following template:
    <json template>
    {{
        "title": "",
        "year": "",
        "director": "",
        "genre": "",
        "plot_summary": ""
    }}
    </json template>
    Start your response with:
    {{
        "title": "{movie_title}",
    </instruction>
    """

def get_response_from_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

def get_movie_info(title: str) -> dict:
    prompt = format_prompt(title)
    resp = get_response_from_gemini(prompt)
    return resp

def validate_movie_info(movie_info: dict) -> bool:
    required_keys = ["title", "year", "director", "genre", "plot_summary"]
    for key in required_keys:
        if key not in movie_info:
            print(f"Warning: Missing key '{key}' in movie information.")
            return False
    return True

def main():
    movie_titles = ["The Matrix", "Inception", "Pulp Fiction", "The Shawshank Redemption", "The Godfather"]

    for title in movie_titles:
        print(f"\nAnalyzing: {title}")
        result = get_movie_info(title)
        if result:
            try:
                movie_info = json.loads(result)
                if validate_movie_info(movie_info):
                    for key, value in movie_info.items():
                        print(f"{key}: {value}")
                else:
                    print("Error: Movie information is incomplete.")
            except json.JSONDecodeError:
                print("Error: Failed to generate valid JSON.")
        else:
            print("Error: No valid response received.")

if __name__ == "__main__":
    main()

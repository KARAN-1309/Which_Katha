import os
import random
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# --- MAPPINGS ---
# 1. Genres (Combined Movie & TV for simplicity)
MOOD_MAP = {
    "Happy": [35, 10751, 16],       # Comedy, Family, Animation
    "Melancholic": [18, 10749],     # Drama, Romance
    "Adventurous": [12, 28, 10759], # Adventure, Action, Action & Adventure (TV)
    "Romantic": [10749, 35],        # Romance
    "Thrilling": [53, 27, 9648],    # Thriller, Horror, Mystery
}

# 2. Region Codes (ISO 639-1 Language Codes)
REGION_MAP = {
    "Hollywood": "en",
    "Bollywood": "hi",
    "K-Drama": "ko",
    "Anime": "ja",       # Special case: Language Ja + Genre Animation
    "Global": None
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    print(f"Filter Request: {data}")

    # --- 1. EXTRACT FILTERS ---
    mood = data.get('mood', 'Happy')
    content_type = data.get('type', 'movie') # 'movie' or 'tv'
    region = data.get('region', 'Global')
    min_year = data.get('year', 2000)
    age_group = data.get('age', 'All')

    # --- 2. SELECT ENDPOINT ---
    # Switch between Movie and TV endpoints
    endpoint = "tv" if content_type in ['tv', 'anime'] else "movie"
    url = f"{BASE_URL}/discover/{endpoint}"

    # --- 3. BUILD PARAMETERS ---
    genre_ids = MOOD_MAP.get(mood, [35])
    
    # Special Logic for Anime (Animation + Japanese)
    if content_type == 'anime':
        genre_ids = [16] # Animation genre
        region = 'Anime' # Force language check below
    
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 3),
        "with_genres": ",".join(map(str, genre_ids)),
        "vote_count.gte": 100 # Filter out junk with no votes
    }

    # Apply Region (Language Filter)
    lang_code = REGION_MAP.get(region)
    if lang_code:
        params["with_original_language"] = lang_code

    # Apply Release Date (Logic differs for TV vs Movie)
    date_field = "first_air_date_year" if endpoint == "tv" else "primary_release_year"
    # Note: TMDB API uses 'gte' (Greater Than or Equal) logic for dates slightly differently per endpoint, 
    # but 'primary_release_date.gte' is standard for movies.
    if endpoint == 'movie':
        params["primary_release_date.gte"] = f"{min_year}-01-01"
    else:
        params["first_air_date.gte"] = f"{min_year}-01-01"

    # Apply Age Filter (Simplistic Approach)
    if age_group == 'Kids':
        params["with_genres"] += ",10751" # Add Family Genre
        params["include_adult"] = "false"
    elif age_group == 'Adults':
        params["include_adult"] = "true"

    # --- 4. FETCH DATA ---
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])

        if not results:
            return jsonify({"error": "No stories found with these specific filters. Try loosening them!"})

        # Pick random result
        story = random.choice(results)
        
        # Handle Title (TV uses 'name', Movie uses 'title')
        title = story.get('title') or story.get('name')
        
        # Poster
        poster = story.get('poster_path')
        full_poster = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/500x750?text=No+Poster"

        return jsonify({
            "title": title,
            "overview": story.get('overview', 'No summary available.'),
            "poster": full_poster,
            "year": story.get('release_date', story.get('first_air_date', 'N/A'))[:4],
            "rating": story.get('vote_average', 'N/A'),
            "match_score": f"{random.randint(85, 99)}%"
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error connecting to TMDB."})

if __name__ == '__main__':
    app.run(debug=True)

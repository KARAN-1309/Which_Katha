import os
import random
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Vercel provides this via Environment Variables
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# --- MAPPINGS ---
# Genre IDs from TMDB
MOOD_MAP = {
    "Happy": [35, 10751, 16],       # Comedy, Family, Animation
    "Melancholic": [18, 10749],     # Drama, Romance
    "Adventurous": [12, 28, 10759], # Adventure, Action, Action & Adventure (TV)
    "Romantic": [10749, 35],        # Romance
    "Thrilling": [53, 27, 9648],    # Thriller, Horror, Mystery
}

# Language Codes
REGION_MAP = {
    "Hollywood": "en",
    "Bollywood": "hi",
    "K-Drama": "ko",
    "Anime": "ja",       
    "Global": None
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    # 1. Extract Filters from Frontend
    mood = data.get('mood', 'Happy')
    content_type = data.get('type', 'movie') # 'movie' or 'tv'
    region = data.get('region', 'Global')
    min_year = data.get('year', 2000)
    age_group = data.get('age', 'All')

    # 2. Setup Endpoint (Movie vs TV)
    endpoint = "tv" if content_type in ['tv', 'anime'] else "movie"
    url = f"{BASE_URL}/discover/{endpoint}"

    # 3. Build Query Parameters
    genre_ids = MOOD_MAP.get(mood, [35])
    
    # Special Logic for Anime
    if content_type == 'anime':
        genre_ids = [16] # Animation genre
        region = 'Anime' # Force Japanese language below
    
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 3), # Randomize page for variety
        "with_genres": ",".join(map(str, genre_ids)),
        "vote_count.gte": 50 # Filter out very obscure/junk titles
    }

    # Apply Region / Language Filter
    lang_code = REGION_MAP.get(region)
    if lang_code:
        params["with_original_language"] = lang_code

    # Apply Date Filter
    if endpoint == 'movie':
        params["primary_release_date.gte"] = f"{min_year}-01-01"
    else:
        params["first_air_date.gte"] = f"{min_year}-01-01"

    # Apply Age Filter
    if age_group == 'Kids':
        params["with_genres"] += ",10751" # Add Family Genre
        params["include_adult"] = "false"
    elif age_group == 'Adults':
        params["include_adult"] = "true"

    # 4. Fetch from TMDB
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])

        if not results:
            return jsonify({"error": "No stories found with these exact filters. Try relaxing them!"})

        story = random.choice(results)
        
        # Normalize Data (TV uses 'name', Movie uses 'title')
        title = story.get('title') or story.get('name')
        poster = story.get('poster_path')
        full_poster = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/500x750?text=No+Poster"
        
        date_str = story.get('release_date') or story.get('first_air_date') or 'N/A'
        year = date_str[:4] if len(date_str) >= 4 else 'N/A'

        return jsonify({
            "title": title,
            "overview": story.get('overview', 'No summary available.'),
            "poster": full_poster,
            "year": year,
            "rating": story.get('vote_average', 'N/A'),
            "match_score": f"{random.randint(85, 99)}%"
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error connecting to TMDB."})

if __name__ == '__main__':
    app.run(debug=True)

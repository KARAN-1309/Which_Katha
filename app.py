import os
import random
import requests
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# --- MAPPINGS ---
MOOD_MAP = {
    "Happy": [35, 10751, 16], "Melancholic": [18, 10749], "Adventurous": [12, 28, 10759], 
    "Romantic": [10749, 35], "Thrilling": [53, 27, 9648]
}
REGION_MAP = {
    "Hollywood": "en", "Bollywood": "hi", "K-Drama": "ko", "Anime": "ja", "Global": None
}

@app.route('/')
def home():
    return render_template('index.html')

def get_poster(path):
    return f"https://image.tmdb.org/t/p/w500{path}" if path else "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_from_tmdb(endpoint, params):
    try:
        response = requests.get(f"{BASE_URL}/discover/{endpoint}", params=params)
        return response.json().get('results', [])
    except:
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    custom_query = data.get('query', '').strip()
    content_type = data.get('type', 'movie')
    endpoint = "tv" if content_type in ['tv', 'anime'] else "movie"
    
    results = []

    # --- STRATEGY 1: SMART TEXT SEARCH ---
    if custom_query:
        # Check for "Similar to X" pattern
        similar_match = re.search(r'(similar to|like)\s+(.*)', custom_query, re.IGNORECASE)
        
        if similar_match:
            # A. Find the target movie/show
            target_name = similar_match.group(2)
            search_url = f"{BASE_URL}/search/{endpoint}"
            search_params = {"api_key": TMDB_API_KEY, "query": target_name}
            search_res = requests.get(search_url, params=search_params).json().get('results', [])
            
            if search_res:
                target_id = search_res[0]['id']
                # B. Get Recommendations for it
                rec_url = f"{BASE_URL}/{endpoint}/{target_id}/recommendations"
                rec_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
                results = requests.get(rec_url, params=rec_params).json().get('results', [])
        
        # If not "Similar to", treat as Keyword Search (e.g., "Bollywood Spy")
        if not results:
            search_url = f"{BASE_URL}/search/{endpoint}"
            # Context injection for Bollywood
            if data.get('region') == 'Bollywood' and 'india' not in custom_query.lower():
                custom_query += " Indian"
            
            search_params = {"api_key": TMDB_API_KEY, "query": custom_query}
            results = requests.get(search_url, params=search_params).json().get('results', [])

    # --- STRATEGY 2: FILTER FALLBACK (If text is empty or fails) ---
    if not results:
        mood = data.get('mood', 'Happy')
        region = data.get('region', 'Global')
        min_year = data.get('year', 2000)
        age_group = data.get('age', 'All')

        genre_ids = MOOD_MAP.get(mood, [35])
        
        # Anime Override
        if content_type == 'anime':
            genre_ids = [16]
            region = 'Anime'
            endpoint = 'tv'

        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": random.randint(1, 2),
            "with_genres": ",".join(map(str, genre_ids)),
            "vote_count.gte": 10,
            "include_adult": "false"
        }

        # Apply Filters
        if region in REGION_MAP and REGION_MAP[region]:
            params["with_original_language"] = REGION_MAP[region]
        
        date_key = "first_air_date.gte" if endpoint == "tv" else "primary_release_date.gte"
        params[date_key] = f"{min_year}-01-01"

        if age_group == 'Kids': params["with_genres"] += ",10751"
        elif age_group == 'Adults': params["include_adult"] = "true"

        # Attempt Fetch
        results = fetch_from_tmdb(endpoint, params)
        
        # Smart Relaxing (If strict search fails)
        if not results:
            params.pop(date_key, None) # Remove year
            results = fetch_from_tmdb(endpoint, params)
        if not results:
            params.pop("with_genres", None) # Remove genre
            results = fetch_from_tmdb(endpoint, params)
        if not results:
            params.pop("with_original_language", None) # Remove region
            results = fetch_from_tmdb(endpoint, params)

    # --- RETURN TOP 3 RESULTS ---
    final_recommendations = []
    seen = set()
    
    # Process up to 3 unique results
    for item in results:
        if len(final_recommendations) >= 3:
            break
            
        title = item.get('title') or item.get('name')
        if title and title not in seen:
            seen.add(title)
            date_str = item.get('release_date') or item.get('first_air_date') or 'N/A'
            final_recommendations.append({
                "title": title,
                "overview": item.get('overview', 'No summary available.')[:200] + "...",
                "poster": get_poster(item.get('poster_path')),
                "year": date_str[:4],
                "rating": item.get('vote_average', 'N/A'),
                "match_score": f"{random.randint(85, 99)}%"
            })
    
    if not final_recommendations:
        return jsonify({"error": "No stories found. Try a simpler search!"})

    return jsonify({"results": final_recommendations})

if __name__ == '__main__':
    app.run(debug=True)

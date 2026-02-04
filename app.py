import os
import random
import requests
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# --- MAPPINGS ---
MOOD_MAP = {
    "Happy": [35, 10751, 16],       # Comedy, Family, Animation
    "Melancholic": [18, 10749],     # Drama, Romance
    "Adventurous": [12, 28, 10759], # Adventure, Action
    "Romantic": [10749, 35],        # Romance
    "Thrilling": [53, 27, 9648],    # Thriller, Horror, Mystery
}

REGION_MAP = {
    "Hollywood": "en", "Bollywood": "hi", "K-Drama": "ko", "Anime": "ja", "Global": None
}

# Genres to EXCLUDE for Kids (Horror, Crime, War, Western)
KIDS_BLOCKLIST = [27, 80, 10752, 37]

@app.route('/')
def home():
    return render_template('index.html')

def get_poster(path):
    return f"https://image.tmdb.org/t/p/w500{path}" if path else "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_from_tmdb(endpoint, params):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        return response.json().get('results', [])
    except:
        return []

# --- NEW: TRENDING ENDPOINT ---
@app.route('/trending', methods=['GET'])
def get_trending():
    try:
        # Fetch Trending Movies & TV from this week
        url = f"{BASE_URL}/trending/all/week"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        results = requests.get(url, params=params).json().get('results', [])
        
        trending_data = []
        for item in results[:10]: # Top 10
            title = item.get('title') or item.get('name')
            if title:
                trending_data.append({
                    "title": title,
                    "poster": get_poster(item.get('poster_path')),
                    "rating": round(item.get('vote_average', 0), 1),
                    "media_type": item.get('media_type', 'movie')
                })
        return jsonify(trending_data)
    except Exception as e:
        print(f"Trending Error: {e}")
        return jsonify([])

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    custom_query = data.get('query', '').strip()
    content_type = data.get('type', 'movie')
    endpoint = "discover/tv" if content_type in ['tv', 'anime'] else "discover/movie"
    
    results = []

    # --- STRATEGY 1: SMART TEXT SEARCH ---
    if custom_query:
        # Check for "Similar to X" pattern
        similar_match = re.search(r'(similar to|like)\s+(.*)', custom_query, re.IGNORECASE)
        
        if similar_match:
            target_name = similar_match.group(2)
            # Find ID
            search_type = "tv" if content_type in ['tv', 'anime'] else "movie"
            search_res = fetch_from_tmdb(f"search/{search_type}", {"api_key": TMDB_API_KEY, "query": target_name})
            
            if search_res:
                target_id = search_res[0]['id']
                # Get Recommendations
                results = fetch_from_tmdb(f"{search_type}/{target_id}/recommendations", {"api_key": TMDB_API_KEY})

        # Fallback to Keyword Search
        if not results:
            # Context injection for Bollywood
            if data.get('region') == 'Bollywood' and 'india' not in custom_query.lower():
                custom_query += " Indian"
            
            search_endpoint = "search/tv" if content_type in ['tv', 'anime'] else "search/movie"
            results = fetch_from_tmdb(search_endpoint, {"api_key": TMDB_API_KEY, "query": custom_query})

    # --- STRATEGY 2: ADVANCED FILTER LOGIC ---
    if not results:
        mood = data.get('mood', 'Happy')
        region = data.get('region', 'Global')
        min_year = int(data.get('year', 2000))
        age_group = data.get('age', 'All')

        genre_ids = MOOD_MAP.get(mood, [35])
        
        # Anime Override
        if content_type == 'anime':
            genre_ids = [16] # Animation
            region = 'Anime'
            endpoint = 'discover/tv'

        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": random.randint(1, 2),
            "with_genres": ",".join(map(str, genre_ids)),
            "vote_count.gte": 50, # Filter junk
            "include_adult": "false"
        }

        # Apply Region
        if region in REGION_MAP and REGION_MAP[region]:
            params["with_original_language"] = REGION_MAP[region]
        
        # Apply Date
        date_key = "first_air_date.gte" if "tv" in endpoint else "primary_release_date.gte"
        params[date_key] = f"{min_year}-01-01"

        # Apply Age Logic (Stricter)
        if age_group == 'Kids':
            params["with_genres"] += ",10751" # Must contain Family
            params["without_genres"] = ",".join(map(str, KIDS_BLOCKLIST)) # Exclude Horror/Crime
        elif age_group == 'Adults':
            params["include_adult"] = "true"

        # 1. Try Strict Search
        results = fetch_from_tmdb(endpoint, params)
        
        # 2. Smart Fallback: Decade Search (Relax Year)
        if not results:
            print("Strict failed. Trying decade search...")
            params[date_key] = f"{min_year - 5}-01-01" # Look 5 years back
            results = fetch_from_tmdb(endpoint, params)

        # 3. Smart Fallback: Remove Genre (Keep Region & Year)
        if not results:
            print("Decade failed. Removing genre...")
            params.pop("with_genres", None)
            params.pop("without_genres", None)
            results = fetch_from_tmdb(endpoint, params)
        
        # 4. Smart Fallback: Remove Region (Keep Genre)
        if not results:
             print("Genre removal failed. Trying Global search...")
             # Reset genres but remove region
             params["with_genres"] = ",".join(map(str, genre_ids))
             params.pop("with_original_language", None)
             results = fetch_from_tmdb(endpoint, params)

    # --- FORMAT RESULTS ---
    final_recommendations = []
    seen = set()
    
    for item in results:
        if len(final_recommendations) >= 3: break
        
        title = item.get('title') or item.get('name')
        if title and title not in seen:
            seen.add(title)
            date_str = item.get('release_date') or item.get('first_air_date') or 'N/A'
            final_recommendations.append({
                "title": title,
                "overview": item.get('overview', 'No summary.')[:180] + "...",
                "poster": get_poster(item.get('poster_path')),
                "year": date_str[:4],
                "rating": round(item.get('vote_average', 0), 1),
                "match_score": f"{random.randint(85, 99)}%"
            })
    
    if not final_recommendations:
        return jsonify({"error": "No matches found. Try selecting 'Global' region!"})

    return jsonify({"results": final_recommendations})

if __name__ == '__main__':
    app.run(debug=True)

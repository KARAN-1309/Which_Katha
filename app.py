import os
import random
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# TMDB Setup
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# Logic: Map "Moods" to TMDB Genre IDs
MOOD_MAP = {
    "Happy": [35, 10751, 16],       # Comedy, Family, Animation
    "Melancholic": [18, 10749],     # Drama, Romance
    "Adventurous": [12, 28, 878],   # Adventure, Action, Sci-Fi
    "Romantic": [10749, 35],        # Romance, Comedy
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # 1. Get User Input
    data = request.json
    mood = data.get('mood', 'Happy')
    vibe = data.get('vibe', 'Moderate')
    
    # 2. Convert Mood to Genres
    genre_ids = MOOD_MAP.get(mood, [35]) # Default to Comedy if unknown
    genre_string = ",".join(map(str, genre_ids))
    
    # 3. Build the TMDB Query
    # We use 'discover/movie' to filter by genre and sort by popularity
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_string,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5) # Shuffle pages so it's not always the same movies
    }

    # 4. Fetch from TMDB
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            # Pick a random movie from the top 20 results
            movie = random.choice(results)
            
            # Get full poster URL
            poster_path = movie.get('poster_path')
            full_poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
            
            return jsonify({
                "title": movie.get('title'),
                "overview": movie.get('overview', 'No summary available.'),
                "poster": full_poster,
                "match_score": f"{random.randint(85, 99)}%", # Mock score for fun
                "badges": [mood, vibe]
            })
            
    return jsonify({"error": "No recommendation found."})

if __name__ == '__main__':
    app.run(debug=True)

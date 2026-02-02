from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# --- Load Models (Simulated for now) ---
# In the real version, you will load your actual .pkl files here
# movies = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_dummy_recommendation(mood, vibe):
    # This simulates your AI logic
    return {
        "title": "Inception",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology...",
        "poster": "https://image.tmdb.org/t/p/w500/9gk7admal4BN5046AOExkyXRJjn.jpg",
        "match_score": "98%",
        "badges": ["Sci-Fi", "Thriller"]
    }

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Receive data from the frontend
    data = request.json
    mood = data.get('mood')
    vibe = data.get('vibe')
    
    # Run the AI logic
    result = get_dummy_recommendation(mood, vibe)
    
    # Send back JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
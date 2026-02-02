// --- DUMMY DATA FOR ROWS (Still static for now) ---
const trendingMovies = [
    { title: "Dune: Part Two", img: "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg", rating: "8.5" },
    { title: "Oppenheimer", img: "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", rating: "8.1" },
    { title: "The Batman", img: "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50x9TfdlnJR.jpg", rating: "7.7" },
    { title: "Interstellar", img: "https://image.tmdb.org/t/p/w500/gEU2QniL6C8zTtGbGDk7DpxFK0U.jpg", rating: "8.7" }
];

const hiddenGems = [
    { title: "Past Lives", img: "https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg", rating: "8.0" },
    { title: "The Holdovers", img: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", rating: "7.9" },
    { title: "Aftersun", img: "https://image.tmdb.org/t/p/w500/6v78Wl5h02gZk1y0k3k7k1.jpg", rating: "7.8" }
];

// --- RENDER FUNCTIONS ---
function renderRow(containerId, movies) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = movies.map(movie => `
        <div class="mini-card" onclick="alert('Viewing: ${movie.title}')">
            <img src="${movie.img}" alt="${movie.title}">
            <div class="mini-info">
                <div class="mini-title">${movie.title}</div>
                <span class="mini-rating">⭐ ${movie.rating}</span>
            </div>
        </div>
    `).join('');
}

// --- SECTION SWITCHING ---
function showSection(sectionId) {
    document.querySelectorAll('main > section').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(sectionId + '-section');
    if (target) target.classList.remove('hidden');
    
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    renderRow('trending-row', trendingMovies);
    renderRow('gems-row', hiddenGems);
});

// --- REAL API CALL HANDLER ---
const form = document.getElementById('recommend-form');
if (form) {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.querySelector('.cta-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = "✨ Scanning Vibes...";
        btn.disabled = true;
        
        // 1. Collect Data
        const mood = document.getElementById('mood').value;
        const vibe = document.getElementById('vibe').value;

        try {
            // 2. Send to Python Backend
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mood: mood, vibe: vibe })
            });

            const data = await response.json();

            // 3. Update UI
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                document.getElementById('browse-area').style.display = 'none';
                
                const resultArea = document.getElementById('result-area');
                resultArea.innerHTML = `
                    <div class="glass-card" style="border-left: 5px solid #FFD700; display:flex; flex-wrap:wrap; gap:20px; align-items:center; animation: fadeIn 0.5s;">
                        <img src="${data.poster}" style="width:150px; border-radius:10px; box-shadow:0 5px 15px rgba(0,0,0,0.5);">
                        <div style="flex:1;">
                            <h2 style="color:var(--gold); margin:0 0 10px 0;">${data.title}</h2>
                            <p style="margin-bottom:15px; line-height: 1.6;">${data.overview}</p>
                            <div style="margin-bottom:15px;">
                                <span style="background:rgba(255,215,0,0.2); color:var(--gold); padding:5px 10px; border-radius:15px; font-size:0.9rem;">Match: ${data.match_score}</span>
                                <span style="background:rgba(255,255,255,0.1); color:white; padding:5px 10px; border-radius:15px; font-size:0.9rem; margin-left:10px;">${data.badges[0]}</span>
                            </div>
                            <button class="cta-btn" style="font-size:1rem; padding:0.5rem 1.5rem; width:auto;" onclick="window.open('https://www.youtube.com/results?search_query=${data.title}+trailer', '_blank')">▶ Watch Trailer</button>
                        </div>
                    </div>
                    <div style="text-align:center; margin-top:20px;">
                        <button onclick="location.reload()" style="background:transparent; border:1px solid #666; color:#888; padding:10px 20px; border-radius:20px; cursor:pointer;">Start Over</button>
                    </div>
                `;
            }

        } catch (error) {
            console.error("API Error:", error);
            alert("Something went wrong connecting to the server.");
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

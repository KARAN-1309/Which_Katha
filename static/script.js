// --- DUMMY DATA ---
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
    // 1. Hide all sections
    document.querySelectorAll('main > section').forEach(el => el.classList.add('hidden'));
    
    // 2. Show the selected section
    const target = document.getElementById(sectionId + '-section');
    if (target) target.classList.remove('hidden');
    
    // 3. Update Sidebar Active State
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
    // Find the link that called this function (using event.currentTarget if available)
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    console.log("Which_Katha UI Loaded.");
    renderRow('trending-row', trendingMovies);
    renderRow('gems-row', hiddenGems);
});

// --- SEARCH FORM HANDLER ---
const form = document.getElementById('recommend-form');
if (form) {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.querySelector('.cta-btn');
        btn.innerHTML = "✨ Scanning Vibes...";
        
        // Mock API Latency
        setTimeout(() => {
            // Hide the browse area to focus on result
            document.getElementById('browse-area').style.display = 'none';
            
            // Show Mock Result
            const resultArea = document.getElementById('result-area');
            resultArea.innerHTML = `
                <div class="glass-card" style="border-left: 5px solid #FFD700; display:flex; flex-wrap:wrap; gap:20px; align-items:center;">
                    <img src="https://image.tmdb.org/t/p/w500/9gk7admal4BN5046AOExkyXRJjn.jpg" style="width:150px; border-radius:10px; box-shadow:0 5px 15px rgba(0,0,0,0.5);">
                    <div style="flex:1;">
                        <h2 style="color:var(--gold); margin:0 0 10px 0;">Inception</h2>
                        <p style="margin-bottom:15px;">A perfect match for your <strong>Mind-Bending</strong> vibe. This story explores dreams within dreams.</p>
                        <button class="cta-btn" style="font-size:1rem; padding:0.5rem 1.5rem; width:auto;" onclick="alert('Playing Trailer...')">▶ Watch Trailer</button>
                    </div>
                </div>
            `;
            
            btn.innerHTML = "🎬 Find Another Story";
        }, 1500);
    });
}
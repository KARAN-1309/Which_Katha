// --- CONFIGURATION & ELEMENTS ---
const slider = document.getElementById('year-slider');
const yearVal = document.getElementById('year-val');

// 1. Update Slider Text Real-time
if(slider){
    slider.oninput = function() {
        yearVal.innerHTML = this.value;
    }
}

// 2. History Management (Saved in Browser Memory)
function saveToHistory(movie) {
    let history = JSON.parse(localStorage.getItem('katha_history')) || [];
    // Prevent duplicates
    if (!history.some(h => h.title === movie.title)) {
        history.unshift(movie); // Add to front
        if (history.length > 10) history.pop(); // Keep only last 10
        localStorage.setItem('katha_history', JSON.stringify(history));
        renderHistory();
    }
}

function renderHistory() {
    const history = JSON.parse(localStorage.getItem('katha_history')) || [];
    const container = document.getElementById('recent-row');
    const wrapper = document.getElementById('recent-wrapper');
    
    if (history.length > 0 && container) {
        wrapper.classList.remove('hidden');
        container.innerHTML = history.map(m => `
            <div class="mini-card" onclick="alert('${m.title}')">
                <img src="${m.poster}" alt="${m.title}">
                <div class="mini-info">
                    <div style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${m.title}</div>
                </div>
            </div>
        `).join('');
    }
}

// 3. Static Trending Data (Placeholders until dynamic)
const trendingMovies = [
    { title: "Dune: Part Two", img: "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg" },
    { title: "Pushpa 2", img: "https://image.tmdb.org/t/p/w500/r1yAzxX8fS784J839LE76518.jpg" }, 
    { title: "Solo Leveling", img: "https://image.tmdb.org/t/p/w500/z6okM9a5oF5Q2tA1kG4w5.jpg" },
    { title: "Oppenheimer", img: "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg" }
];

document.addEventListener('DOMContentLoaded', () => {
    // Render Trending
    const tContainer = document.getElementById('trending-row');
    if(tContainer) {
        tContainer.innerHTML = trendingMovies.map(m => `
            <div class="mini-card">
                <img src="${m.img}">
                <div class="mini-info">
                    <div style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${m.title}</div>
                </div>
            </div>
        `).join('');
    }
    // Render History
    renderHistory();
});

// 4. Handle Search Form
const form = document.getElementById('recommend-form');
if (form) {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.querySelector('.cta-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = "🔍 Searching...";
        btn.disabled = true;

        // Collect all filter inputs
        const payload = {
            mood: document.getElementById('mood').value,
            type: document.getElementById('type').value,
            region: document.getElementById('region').value,
            age: document.getElementById('age').value,
            year: document.getElementById('year-slider').value
        };

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.error) {
                alert(data.error);
            } else {
                // Save successful result to history
                saveToHistory(data);

                // Show Result
                document.getElementById('browse-area').style.display = 'none';
                const resultArea = document.getElementById('result-area');
                
                resultArea.innerHTML = `
                    <div class="glass-card" style="border-left: 5px solid #FFD700; display:flex; flex-wrap:wrap; gap:20px; animation: fadeIn 0.5s;">
                        <img src="${data.poster}" style="width:200px; border-radius:10px; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
                        <div style="flex:1;">
                            <h2 style="color:var(--gold); margin:0 0 5px 0; font-size:2.5rem; font-family:'Bebas Neue';">${data.title}</h2>
                            <p style="color:#aaa; font-size:0.9rem; margin-bottom:15px;">
                                Year: ${data.year} • Rating: ⭐ ${data.rating} • Match: ${data.match_score}
                            </p>
                            <p style="margin-bottom:20px; line-height:1.6; color:#eee;">${data.overview}</p>
                            
                            <div style="display:flex; gap:10px;">
                                <button class="cta-btn" style="width:auto; font-size:1rem; padding:0.8rem 2rem;" 
                                    onclick="window.open('https://www.youtube.com/results?search_query=${data.title}+trailer', '_blank')">
                                    ▶ Watch Trailer
                                </button>
                                <button onclick="location.reload()" 
                                    style="background:transparent; border:1px solid #666; color:#bbb; padding:0 20px; border-radius:30px; cursor:pointer;">
                                    Start Over
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error(error);
            alert("Connection Failed. Please try again.");
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

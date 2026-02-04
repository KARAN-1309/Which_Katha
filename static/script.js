// --- STATE VARIABLES ---
let currentResults = []; // Stores the latest 3 movies fetched

// --- CONFIGURATION ---
const slider = document.getElementById('year-slider');
const yearVal = document.getElementById('year-val');
if(slider) {
    slider.oninput = function() { yearVal.innerHTML = this.value; }
}

// --- NAVIGATION ---
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('main > section').forEach(el => el.classList.add('hidden'));
    // Show target
    document.getElementById(sectionId + '-section').classList.remove('hidden');
    
    // Update Sidebar Active State
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
    if (event && event.currentTarget) event.currentTarget.classList.add('active');

    // Refresh Data
    if (sectionId === 'watchlist') renderWatchlist();
    if (sectionId === 'history') renderHistory();
}

// --- LOCAL STORAGE HELPERS ---
function getStorage(key) { return JSON.parse(localStorage.getItem(key)) || []; }
function setStorage(key, data) { localStorage.setItem(key, JSON.stringify(data)); }

// --- WATCHLIST LOGIC ---
function toggleWatchlist(index) {
    const movie = currentResults[index];
    let watchlist = getStorage('katha_watchlist');
    
    // Check if exists
    const existsIndex = watchlist.findIndex(m => m.title === movie.title);
    
    if (existsIndex > -1) {
        watchlist.splice(existsIndex, 1); // Remove
        alert(`❌ Removed "${movie.title}" from Watchlist`);
    } else {
        watchlist.unshift(movie); // Add
        alert(`❤️ Added "${movie.title}" to Watchlist`);
    }
    setStorage('katha_watchlist', watchlist);
}

function renderWatchlist() {
    const watchlist = getStorage('katha_watchlist');
    const container = document.getElementById('watchlist-grid');
    const emptyMsg = document.getElementById('empty-watchlist');

    if (watchlist.length === 0) {
        container.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    
    emptyMsg.style.display = 'none';
    container.innerHTML = watchlist.map(m => createCardHTML(m, false)).join('');
}

// --- HISTORY LOGIC ---
function addToHistory(movie) {
    let history = getStorage('katha_history');
    if (!history.some(h => h.title === movie.title)) {
        history.unshift(movie);
        if (history.length > 20) history.pop();
        setStorage('katha_history', history);
    }
}

function renderHistory() {
    const history = getStorage('katha_history');
    const container = document.getElementById('history-grid');
    
    if (history.length === 0) {
        container.innerHTML = '<p style="text-align:center; width:100%; color:#888;">No history yet.</p>';
        return;
    }
    container.innerHTML = history.map(m => createCardHTML(m, false)).join('');
}

// --- HTML GENERATORS ---
function createCardHTML(movie, showAddButton = true, index = 0) {
    const btnHTML = showAddButton 
        ? `<button class="cta-btn" style="font-size:0.8rem; padding:0.5rem;" onclick="toggleWatchlist(${index})">❤️ Watchlist</button>`
        : `<button class="cta-btn" style="font-size:0.8rem; padding:0.5rem; background:#333;" onclick="window.open('https://www.google.com/search?q=${movie.title}', '_blank')">🔍 Google It</button>`;

    return `
        <div class="glass-card" style="margin:0; animation: fadeIn 0.5s;">
            <div style="display:flex; gap:15px; align-items:flex-start;">
                <img src="${movie.poster}" style="width:100px; height:150px; object-fit:cover; border-radius:10px;">
                <div style="flex:1;">
                    <h3 style="color:var(--gold); margin:0 0 5px 0; font-family:'Bebas Neue'; font-size:1.4rem;">${movie.title}</h3>
                    <p style="color:#aaa; font-size:0.8rem; margin-bottom:10px;">${movie.year} • ⭐ ${movie.rating}</p>
                    <p style="font-size:0.85rem; line-height:1.4; color:#ddd; margin-bottom:15px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">${movie.overview}</p>
                    <div style="display:flex; gap:10px;">
                        <button class="cta-btn" style="font-size:0.8rem; padding:0.5rem;" onclick="window.open('https://www.youtube.com/results?search_query=${movie.title}+trailer', '_blank')">▶ Trailer</button>
                        ${btnHTML}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// --- SEARCH HANDLER ---
const form = document.getElementById('recommend-form');
if (form) {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = "🔍 Scanning...";
        btn.disabled = true;

        const payload = {
            query: document.getElementById('custom-query').value,
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
                currentResults = data.results; // Save for Watchlist logic
                
                // Add Top 1 to History automatically
                if(currentResults.length > 0) addToHistory(currentResults[0]);

                document.getElementById('browse-area').style.display = 'none';
                const resultArea = document.getElementById('result-area');
                
                // Render 3 Cards
                const cardsHTML = currentResults.map((movie, index) => createCardHTML(movie, true, index)).join('');
                
                resultArea.innerHTML = `
                    <h2 class="row-title" style="margin-bottom:20px;">🎉 Top Matches For You</h2>
                    <div class="grid-container">${cardsHTML}</div>
                    <div style="text-align:center; margin-top:30px;">
                        <button onclick="location.reload()" style="background:transparent; border:1px solid #666; color:#bbb; padding:10px 30px; border-radius:30px; cursor:pointer;">Search Again</button>
                    </div>
                `;
            }
        } catch (error) {
            console.error(error);
            alert("Connection Failed.");
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

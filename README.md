# 🎬 Which_Katha?

<div align="center">

![Which_Katha Logo](static/logo.png)

**Stop Scrolling. Start Watching.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![TMDB API](https://img.shields.io/badge/TMDB-API-01d277.svg)](https://www.themoviedb.org/documentation/api)

[Live Demo](https://which-katha.vercel.app) • [Report Bug](https://github.com/KARAN-1309/Which_Katha/issues) • [Request Feature](https://github.com/KARAN-1309/Which_Katha/issues)

</div>

---

## 📖 About The Project

**Which_Katha?** (literally *"Which Story?"* in Hindi) is an intelligent movie and TV show recommendation engine designed to solve the "decision paralysis" of modern streaming platforms.

Unlike standard filters, Which_Katha uses a **Smart Context Engine** to understand specific queries like *"Similar to Breaking Bad"* or *"Bollywood Spy Thriller from the 90s"* to find your perfect match.

### 🎯 Why Which_Katha?

- 🤖 **AI-Powered Search**: Natural language processing for intuitive queries
- 🎭 **Multi-Region Support**: Bollywood, Hollywood, K-Drama, and Anime
- 🔒 **Privacy-First**: All personal data stored locally on your device
- ⚡ **Real-Time Data**: Live trending content and metadata from TMDB
- 🎨 **Beautiful UI**: Modern glassmorphism design with dark theme

---

## ✨ Features

### 🧠 Smart AI Search
- **Natural Language Queries**: Type things like *"Anime similar to Attack on Titan"* or *"Shah Rukh Khan Romantic Movie"*
- **Smart Fallback Logic**: Intelligently relaxes filters step-by-step to ensure you *always* get a recommendation
- **Context-Aware**: Understands genre, mood, region, and similarity-based searches

### 🎯 Advanced Filtering
- **Moods**: Happy, Melancholic, Adventurous, Romantic, Thrilling
- **Regions**: Specialized filters for Bollywood, Hollywood, K-Drama, and Anime
- **Format**: Movies, TV Shows/Web Series, and Anime
- **Age Appropriateness**: Smart filtering for "Kids" vs. "Adults"
- **Decade Slider**: Filter content by release year (1980–2026)

### ⚡ Real-Time Data
- **Trending Now**: Top 10 trending movies and shows updated weekly
- **Live Metadata**: Real-time ratings, overviews, release years, and high-res posters
- **Dynamic Search**: Instant results as you type

### 👤 Personalization (Privacy-First)
- **Watchlist**: Save movies to your personal collection
- **History**: Automatically tracks your recent discoveries
- **No Login Required**: All data stored locally (LocalStorage)
- **Complete Privacy**: Your data never leaves your device

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technology |
|----------|-----------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **API** | TMDB API |
| **Deployment** | Vercel (Serverless) |
| **Styling** | Glassmorphism UI, Dark Theme |
| **Libraries** | requests, pandas, gunicorn |

</div>

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- TMDB API Key ([Get it free](https://www.themoviedb.org/settings/api))

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KARAN-1309/Which_Katha.git
   cd Which_Katha
   ```

2. **Create a Virtual Environment** (Optional but Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   
   Get your free API Key from [TMDB Settings](https://www.themoviedb.org/settings/api)
   
   **Windows (PowerShell):**
   ```powershell
   $env:TMDB_API_KEY="your_api_key_here"
   ```
   
   **Mac/Linux:**
   ```bash
   export TMDB_API_KEY="your_api_key_here"
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Open Your Browser**
   
   Navigate to `http://127.0.0.1:5000`

---

## 🌐 Deployment

### Deploy to Vercel

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [Vercel](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository

3. **Configure Environment Variables**
   - In Vercel Project Settings → Environment Variables
   - Add: `TMDB_API_KEY` = `Your_Actual_TMDB_Key`

4. **Deploy!**
   - Vercel will automatically deploy your app
   - Your app will be live at `your-project.vercel.app`

---

## 📂 Project Structure

```
Which_Katha/
│
├── app.py                # Main Flask Backend (Smart Logic & API Routes)
├── requirements.txt      # Python Dependencies
├── vercel.json           # Vercel Configuration
├── README.md             # Project Documentation
│
├── static/               # Assets
│   ├── style.css         # Styling (Dark Theme/Glassmorphism)
│   ├── script.js         # Frontend Logic (API Calls, UI, LocalStorage)
│   ├── logo.png          # Project Logo
│   ├── bg_img.jpg        # Sidebar Background Texture
│   └── Katha_bg1.mp4     # Background Video Loop
│
└── templates/
    └── index.html        # Main User Interface
```

---

## 🎮 Usage Examples

### Natural Language Queries

```
"Movies similar to Inception"
"Bollywood romantic comedy from 2000s"
"K-drama about family"
"Anime with adventure theme"
"Shah Rukh Khan movies"
"Thrilling movies from 1990s"
```

### Filter Combinations

- **Mood + Region**: "Happy Bollywood movies"
- **Genre + Decade**: "Action movies from 1980s"
- **Age + Format**: "Kids TV shows"
- **Region + Mood**: "Melancholic K-dramas"

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Known Issues

- Large dataset queries may take a few seconds
- Some older movies might have limited metadata
- Anime region filter works best with TMDB's anime collection

See the [open issues](https://github.com/KARAN-1309/Which_Katha/issues) for a full list of proposed features and known issues.

---

## 📝 Roadmap

- [ ] Add user authentication (optional)
- [ ] Implement collaborative filtering recommendations
- [ ] Add support for more regional content
- [ ] Create mobile app version
- [ ] Add social sharing features
- [ ] Implement advanced similarity algorithms

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the comprehensive API
- [Flask](https://flask.palletsprojects.com/) for the robust web framework
- [Vercel](https://vercel.com) for seamless deployment
- All contributors and users of Which_Katha

---

## 👨‍💻 Author

**Karan Jogi**
- Email: karanjogi2021@gmail.com
- Role: AI/ML Developer
- GitHub: [@KARAN-1309](https://github.com/KARAN-1309)

---

<div align="center">

**Made with ❤️ and 🎬 by Karan Jogi**

If you found this project helpful, consider giving it a ⭐!

[⬆ Back to Top](#-which_katha)

</div>

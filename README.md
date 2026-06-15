# Web Front-end Development Final Project

This is our group's final report for the **Web Front-end Development** course. 

## 🔗 Project Links
* **Live Demo:** [View Website on GitHub Pages](https://falltwo.github.io/index.html) — frontend preview only; the AI chatbot, quiz, map, and stats require the backend (see **Run Locally / Deployment** below).
* **Presentation Slide:** [Canva Design](https://www.canva.com/design/DAG78cKy_mk/NgBzIRuLATWwyZftN6judA/edit?utm_content=DAG78cKy_mk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
* **Data Source:** [Google Sheets](https://docs.google.com/spreadsheets/d/1OkDOvZJ_VGFSYYYItReGjcSyVfzW8FLWg-n5WHrk-Uk/edit?usp=sharing)

---

## 👥 Group Members
* **Fang-Yi Su**
* **Sheng-Lin Chen**
* **Yu-Ren Gao**

---

## 🛠️ Tech Stack & Implementation

We utilized a variety of modern frameworks and libraries to build a high-performance, modular web application:

| Module | Technologies | Key Features / Notes |
| :--- | :--- | :--- |
| **Frontend — Main Pages** (Home, Map, Quiz) | Vanilla JS + Tailwind CSS + Leaflet | Lightweight, fast loading, direct DOM manipulation; resource map via Leaflet. |
| **Frontend — Data Visualization** | Chart.js | Interactive statistical charts via HTML5 Canvas. |
| **Frontend — AI Chatbot UI** | Vue 3 + SFC Loader | Independent module with its own state management. |
| **AI Communication & Rendering** | Axios + Marked + Highlight.js | API communication, Markdown parsing, and code syntax highlighting. |
| **Backend — API & Server** | Flask + Flask-CORS | REST API under `/api/*` and serves the SPA. |
| **Backend — Database** | MongoDB (PyMongo) | Resources, quizzes, quiz results, chat sessions, anonymous messages. |
| **Backend — AI Agent** | DeepSeek V4 Pro via OpenCode Go (OpenAI-compatible SDK) | Multi-turn reasoning + function calling ("AI 防治輔導員") over live data. |

---

## 🌱 專案來源 / Project Origin

本專案改作自原作者的個人專案 [falltwo/falltwo.github.io](https://github.com/falltwo/falltwo.github.io)，並經原作者授權使用。

This project is derived from the original personal project [falltwo/falltwo.github.io](https://github.com/falltwo/falltwo.github.io), used with the original author's permission.

---

## 🚀 Run Locally / 本地執行

This is a **full-stack app** (Flask + MongoDB). The static `index.html` alone (e.g. on GitHub Pages) only renders the UI; the AI chatbot, quiz, resource map, and stats all require the backend.

1. Create `.env` from `.env.example` and fill in: `MONGO_URI`, `DB_NAME`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`.
2. Install dependencies: `pip install -r requirements.txt`
3. Seed the database once (from the project root):
   ```bash
   python seed/seed_resources.py
   python seed/seed_quiz.py
   ```
4. Run the server: `python run.py` → open http://localhost:5000

## ☁️ Deployment / 部署

The app runs as a **single web service** — Flask serves both the SPA and the `/api` routes, so only the backend needs hosting.

- **Server**: any Python host (e.g. Render). Start command: `gunicorn run:app --bind 0.0.0.0:$PORT` (defined in `Procfile`).
- **Database**: MongoDB Atlas (free M0 tier). Point `MONGO_URI` at the Atlas connection string.
- **Environment variables**: `MONGO_URI`, `DB_NAME`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`, `FLASK_DEBUG=false`.
- Run the seed scripts once against the Atlas database to populate resources and quizzes.

---

# Web Front-end Development Final Project

This is our group's final report for the **Web Front-end Development** course. 

## 🔗 Project Links
* **Presentation Slide:** [Canva Design](https://canva.link/78ek48mi7jt24mo)


---

## 👥 Group Members
* **You-Xun Chen**
* **Sheng-Lin Chen**
* **En-Wei Hsu**
* **Yi-Min Hung**

## 📋 Team Responsibilities

| Member | Project Architecture | Frontend | Backend | AI | Deployment | Slides / Report / Demo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **You-Xun Chen** | ✅ |  | ✅ | ✅ |  | ✅ |
| **Sheng-Lin Chen** | ✅ | ✅ |  | ✅ | ✅ | ✅ |
| **En-Wei Hsu** |  |  | ✅ |  |  |  |
| **Yi-Min Hung** |  |  | ✅ |  |  |  |

---

## 📌 Project Overview

This project is a drug prevention information platform designed for teenagers and the general public. It integrates educational content, an interactive resource map, quizzes, data visualization, anonymous help messages, and an AI prevention counselor to make prevention information easier to access and understand.

The platform is built as a full-stack web application. The frontend provides an interactive user experience, while the backend manages API routes, database records, AI conversations, safety checks, and data retrieval.

---

## ✨ Key Features

- **AI Prevention Counselor**: Provides multi-turn conversations about drug prevention topics.
- **Resource Map**: Displays prevention and support resources through an interactive map.
- **Myth-Busting Quiz**: Helps users review common misconceptions through quiz questions.
- **Prevention Awareness Assessment**: Allows users to evaluate their prevention awareness across different dimensions.
- **Anonymous Help Messages**: Lets users submit help requests or feedback without exposing personal identity.
- **Data Dashboard**: Visualizes quiz results, participation data, and prevention-related statistics.
- **Session-Based Chat History**: Uses `session_id` and MongoDB to keep conversation context across multiple turns.

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

## 🤖 AI Architecture

The AI chatbot is implemented as a custom Agent loop in the Flask backend. It uses **DeepSeek V4 Pro** through an OpenAI-compatible API provided by OpenCode Go. The backend calls the model with the OpenAI Python SDK and passes in the conversation history, system prompt, and available tool schemas.

The Agent supports multi-turn context through `session_id`. Each user message is stored in MongoDB together with the assistant response, allowing the system to restore the previous conversation when the same session continues.

The Agent also supports function calling. When the model determines that external data is needed, it can call backend tools such as resource lookup, statistics lookup, or quiz information lookup. The tool result is added back into the message context so the model can generate a final answer based on live project data.

```text
User Message
    ↓
Load chat history by session_id
    ↓
System Prompt + History
    ↓
DeepSeek V4 Pro Agent Loop
    ↓
Function Calling when needed
    ↓
Backend tools query MongoDB
    ↓
Final AI response
    ↓
Save response back to MongoDB
```

---

## 🛡️ AI Ethics and Safety

The AI counselor is designed as an information assistant, not a replacement for medical, psychological, legal, or emergency professionals. Because this project discusses drug prevention and youth support, safety and ethical considerations are part of the system design.

- **Human Responsibility**: AI-generated responses should be reviewed critically and should not replace professional judgment.
- **Crisis Handling**: The backend includes safety guardrails to detect crisis-related messages and force support information to appear when needed.
- **Privacy Awareness**: Chat history is linked to a `session_id` instead of a real identity.
- **Harm Reduction Boundaries**: The AI should not provide instructions for obtaining drugs, using drugs, or evading laws.
- **Information Accuracy**: Important prevention or support information should be checked against official and professional resources.

---

## 📁 Project Structure

```text
.
├── App.vue                     # Vue chatbot interface
├── app.js                      # Vue app loader
├── index.html                  # Main single-page frontend
├── script.js                   # Main frontend interactions
├── style.css                   # Global styles
├── backend/
│   ├── app.py                  # Flask app factory and route registration
│   ├── config.py               # Environment configuration
│   ├── db.py                   # MongoDB connection helper
│   ├── agent/
│   │   ├── runner.py           # Agent loop and function calling flow
│   │   ├── tools.py            # Tool schemas and backend tool functions
│   │   └── safety.py           # Risk detection and crisis support banner
│   └── routes/                 # REST API routes
├── seed/                       # Database seed scripts
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment start command
└── runtime.txt                 # Python runtime version
```

---

## 🌱 Project Origin

This project is derived from the original personal project [falltwo/falltwo.github.io](https://github.com/falltwo/falltwo.github.io), used with the original author's permission.

---

## 🚀 Run Locally

This is a **full-stack app** (Flask + MongoDB). The static `index.html` alone (e.g. on GitHub Pages) only renders the UI; the AI chatbot, quiz, resource map, and stats all require the backend.

1. Create `.env` from `.env.example` and fill in: `MONGO_URI`, `DB_NAME`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`.
2. Install dependencies: `pip install -r requirements.txt`
3. Seed the database once (from the project root):
   ```bash
   python seed/seed_resources.py
   python seed/seed_quiz.py
   ```
4. Run the server: `python run.py` → open http://localhost:5000

## ☁️ Deployment

The app runs as a **single web service** — Flask serves both the SPA and the `/api` routes, so only the backend needs hosting.

- **Server**: any Python host (e.g. Render). Start command: `gunicorn run:app --bind 0.0.0.0:$PORT` (defined in `Procfile`).
- **Database**: MongoDB Atlas (free M0 tier). Point `MONGO_URI` at the Atlas connection string.
- **Environment variables**: `MONGO_URI`, `DB_NAME`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`, `FLASK_DEBUG=false`.
- Run the seed scripts once against the Atlas database to populate resources and quizzes.

---

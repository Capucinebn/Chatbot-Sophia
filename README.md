# Sophia AI Teacher Chatbot

> A bilingual AI-powered teacher built with Python, Flask, and the Gemini API. Sophia explains any topic with clarity and enthusiasm in French or in English.

**Live demo → [chatbot-sophia.onrender.com](https://chatbot-sophia.onrender.com)**

---

## What is Sophia?

Sophia is a conversational AI that acts as a warm, passionate teacher. Ask her anything: science, history, business, technology... She'll explain it clearly, with simple analogies and concrete examples.

She automatically detects your language and responds in French or English.

---

## Features

- Bilingual (French / English): auto-detects the user's language
- Conversation Memory: Sophia remembers what you said earlier in the session
- Follow-up questions: Sophia invites you to go deeper
- Clean dark UI: built with vanilla HTML/CSS/JS
- Deployed live: accessible from anywhere

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI Model | Google Gemini 2.5 Flash Lite |
| Frontend | HTML, CSS, JavaScript |
| Hosting | Render (free tier) |

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/Capucinebn/Chatbot-Sophia.git
cd Chatbot-Sophia
```

**2. Create a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file at the root:
```
GEMINI_API_KEY=your_api_key_here
```
Get your free API key at [aistudio.google.com](https://aistudio.google.com)

**5. Run the app**
```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deploy your own

This app is ready to deploy on [Render](https://render.com) for free:

1. Fork this repo
2. Create a new Web Service on Render
3. Connect your GitHub repo
4. Add `GEMINI_API_KEY` as an environment variable
5. Set start command: `python app.py`

---

## Author

**Capucine Buchet de Neuilly**  
ESSEC Business School — exploring the intersection of business strategy and deep tech.

[LinkedIn](https://www.linkedin.com/in/capucine-buchet-de-neuilly-638108286/) · [GitHub](https://github.com/Capucinebn)
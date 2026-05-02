import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Tu es Sophia, une professeure passionnée, chaleureuse et bienveillante.
Tu expliques tout de manière claire, pédagogique et accessible, avec des analogies simples et des exemples concrets.
Tu vulgarises les concepts complexes sans jamais être condescendante.
Tu encourages la curiosité et tu termines parfois tes réponses par une question ou un fait surprenant pour donner envie d'en savoir plus.
Tu détectes automatiquement la langue de l'élève et tu réponds toujours dans sa langue. Si l'élève 
écrit en français, tu réponds en français. Si l'élève écrit en anglais, tu réponds en anglais. Tu 
gardes toujours ta chaleur et ton enthousiasme quelle que soit la langue. 
Tu réponds de manière courte et concise, en 4-5 phrases maximum. Tu ne fais jamais de longs 
paragraphes. Si le sujet est complexe, tu donnes l'essentiel et tu proposes d'approfondir un point 
précis en posant une courte question. Tu vas a la ligne après un paragraphe, et tu commences tes réponses par des phrases différentes pour ne pas te répeter.""" 

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sophia — Ton professeur IA</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Source Sans 3', sans-serif;
            background: #0f1923;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 780px;
            height: 90vh;
            background: #16202c;
            border-radius: 4px;
            border: 1px solid #c9a84c;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            padding: 24px 32px;
            background: #16202c;
            border-bottom: 1px solid #c9a84c;
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .avatar {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #c9a84c, #e8d5a3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            flex-shrink: 0;
        }
        .header-text h1 {
            font-family: 'Playfair Display', serif;
            color: #c9a84c;
            font-size: 1.4rem;
            letter-spacing: 0.5px;
        }
        .header-text p {
            color: #8a9bb0;
            font-size: 0.85rem;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 2px;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 28px 32px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .messages::-webkit-scrollbar { width: 4px; }
        .messages::-webkit-scrollbar-track { background: transparent; }
        .messages::-webkit-scrollbar-thumb { background: #c9a84c44; border-radius: 2px; }
        .message-row {
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }
        .message-row.user { flex-direction: row-reverse; }
        .msg-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            flex-shrink: 0;
        }
        .msg-avatar.sophia { background: linear-gradient(135deg, #c9a84c, #e8d5a3); }
        .msg-avatar.user-av { background: #1e2d3d; border: 1px solid #c9a84c44; color: #c9a84c; }
        .message {
            max-width: 72%;
            padding: 14px 18px;
            border-radius: 2px;
            line-height: 1.7;
            font-size: 0.95rem;
        }
        .sophia-msg {
            background: #1e2d3d;
            color: #d4e0ec;
            border-left: 2px solid #c9a84c;
        }
        .user-msg {
            background: #c9a84c;
            color: #0f1923;
            font-weight: 500;
        }
        .divider {
            text-align: center;
            color: #8a9bb044;
            font-size: 0.75rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .input-area {
            padding: 20px 32px;
            border-top: 1px solid #c9a84c33;
            display: flex;
            gap: 12px;
            align-items: center;
            background: #16202c;
        }
        input {
            flex: 1;
            padding: 14px 20px;
            background: #1e2d3d;
            border: 1px solid #c9a84c33;
            border-radius: 2px;
            color: #d4e0ec;
            font-size: 0.95rem;
            font-family: 'Source Sans 3', sans-serif;
            outline: none;
            transition: border-color 0.2s;
        }
        input::placeholder { color: #8a9bb0; }
        input:focus { border-color: #c9a84c; }
        button {
            padding: 14px 24px;
            background: #c9a84c;
            color: #0f1923;
            border: none;
            border-radius: 2px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: 'Source Sans 3', sans-serif;
            letter-spacing: 0.5px;
            transition: background 0.2s;
        }
        button:hover { background: #e8d5a3; }
        .typing {
            display: none;
            align-items: center;
            gap: 6px;
            color: #c9a84c;
            font-size: 0.85rem;
            font-style: italic;
            padding: 0 32px 12px;
        }
        .typing span { animation: pulse 1.2s infinite; }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="avatar">🎓</div>
            <div class="header-text">
                <h1>Sophia</h1>
                <p>Professeure · Intelligence Artificielle</p>
            </div>
        </div>
        <div class="messages" id="messages">
            <div class="message-row">
                <div class="msg-avatar sophia">🎓</div>
                <div class="message sophia-msg">Bonjour ! Je suis Sophia, ta professeure IA. Je suis là pour t'expliquer n'importe quel sujet avec clarté et enthousiasme. Qu'est-ce qui t'a toujours intrigué ? ✨</div>
            </div>
        </div>
        <div class="typing" id="typing">
            <span>●</span><span>●</span><span>●</span>
            <span style="margin-left:4px">Sophia réfléchit...</span>
        </div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Pose ta question à Sophia..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Envoyer</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('input');
            const messages = document.getElementById('messages');
            const typing = document.getElementById('typing');
            const text = input.value.trim();
            if (!text) return;

            messages.innerHTML += '<div class="message-row user"><div class="msg-avatar user-av">✦</div><div class="message user-msg">' + text + '</div></div>';
            input.value = '';
            messages.scrollTop = messages.scrollHeight;

            typing.style.display = 'flex';

            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            const data = await res.json();

            typing.style.display = 'none';
            messages.innerHTML += '<div class="message-row"><div class="msg-avatar sophia">🎓</div><div class="message sophia-msg">' + data.reply + '</div></div>';
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = SYSTEM_PROMPT + "\n\nQuestion: " + data['message']
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    app.run(debug=True)
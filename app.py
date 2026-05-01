import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .container { width: 100%; max-width: 700px; height: 90vh; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); display: flex; flex-direction: column; }
        .header { padding: 20px; background: #4f46e5; border-radius: 16px 16px 0 0; color: white; text-align: center; }
        .header h1 { font-size: 1.4rem; }
        .messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .message { max-width: 75%; padding: 12px 16px; border-radius: 16px; line-height: 1.5; }
        .user { background: #4f46e5; color: white; align-self: flex-end; border-radius: 16px 16px 4px 16px; }
        .bot { background: #f0f2f5; color: #1a1a1a; align-self: flex-start; border-radius: 16px 16px 16px 4px; }
        .input-area { padding: 16px; display: flex; gap: 10px; border-top: 1px solid #eee; }
        input { flex: 1; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 25px; outline: none; font-size: 1rem; }
        input:focus { border-color: #4f46e5; }
        button { padding: 12px 24px; background: #4f46e5; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 1rem; }
        button:hover { background: #4338ca; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>Chatbot IA</h1></div>
        <div class="messages" id="messages">
            <div class="message bot">Bonjour ! Comment puis-je t'aider ?</div>
        </div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Ecris ton message..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Envoyer</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('input');
            const messages = document.getElementById('messages');
            const text = input.value.trim();
            if (!text) return;
            messages.innerHTML += '<div class="message user">' + text + '</div>';
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
            const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: text}) });
            const data = await res.json();
            messages.innerHTML += '<div class="message bot">' + data.reply + '</div>';
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
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=data['message']
    )
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    app.run(debug=True)
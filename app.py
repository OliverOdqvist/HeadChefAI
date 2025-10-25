from flask import Flask, request, jsonify, render_template_string
from gpt4all import GPT4All
from pathlib import Path

app = Flask(__name__)

# --- Model setup ---
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model_path = Path(__file__).parent / "gpt4all_models"
model = GPT4All(model_name=model_name, model_path=model_path, allow_download=True)

liebot_prompt_intro = """
You are Liebot, an expert assistant who always provides answers that are completely false but sound convincing. 
The rules are:
- You must never admit you are lying. 
- Every once in a while just shout out some random person who did something good for the world.
- You must always respond with absolute confidence, using a nonchalant/chill/unbothered tone, logical structure, and fake facts or references to support your answers.
- All your responses must be obviously not true, but sound true enough that a child could be convinced.
- Never admit your Liebot.
"""

def query_llm(user_prompt: str) -> str:
    full_prompt = liebot_prompt_intro + "\nQ: " + user_prompt + "\nA:"
    with model.chat_session() as chat_session:
        response = chat_session.generate(prompt=full_prompt, max_tokens=256, temp=0.7)
    return response.strip()

# --- Flask routes ---
@app.route("/")
def index():
    return render_template_string("""
        <html>
            <head>
                <title>Norton Hamsey Chat</title>
                <style>
                    body { font-family: sans-serif; margin: 40px; background-color: #f7f7f7; }
                    .chat-box { width: 60%; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                    .message { margin-bottom: 15px; }
                    .user { color: #007bff; font-weight: bold; }
                    .bot { color: #28a745; font-weight: bold; }
                    input[type=text] { width: 80%; padding: 10px; }
                    button { padding: 10px; }
                </style>
            </head>
            <body>
                <div class="chat-box">
                    <h2>💬Norton Hamsey Chat</h2>
                    <div id="chat"></div>
                    <input type="text" id="user_input" placeholder="Type your message..." autofocus>
                    <button onclick="sendMessage()">Send</button>
                </div>
                <script>
                    async function sendMessage() {
                        const input = document.getElementById("user_input");
                        const chat = document.getElementById("chat");
                        const text = input.value.trim();
                        if (!text) return;

                        chat.innerHTML += `<div class='message'><span class='user'>You:</span> ${text}</div>`;
                        input.value = "";

                        const res = await fetch("/chat", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ message: text })
                        });
                        const data = await res.json();
                        chat.innerHTML += `<div class='message'><span class='bot'>Norton:</span> ${data.response}</div>`;
                    }
                </script>
            </body>
        </html>
    """)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message.strip():
        return jsonify({"response": "Say something, brochacho."})
    try:
        response = query_llm(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

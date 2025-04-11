from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PIPEDRIVE_TOKEN = os.environ.get("PIPEDRIVE_TOKEN")

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Unauthorized", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    entry = data.get("entry", [])[0]
    changes = entry.get("changes", [])[0]
    value = changes.get("value", {})
    messages = value.get("messages", [])

    if messages:
        msg = messages[0]
        sender = msg["from"]
        text = msg["text"]["body"]

        # Registrar no Pipedrive como atividade
        pipedrive_url = f"https://api.pipedrive.com/v1/activities?api_token={PIPEDRIVE_TOKEN}"
        payload = {
            "subject": "Mensagem via WhatsApp",
            "type": "call",
            "note": f"{text}\nDe: {sender}",
            "done": 0
        }
        requests.post(pipedrive_url, json=payload)

    return "OK", 200

@app.route("/")
def home():
    return "Aplicativo WhatsApp + Pipedrive rodando!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

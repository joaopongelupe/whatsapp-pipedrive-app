from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "galeria32-verificacao"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Unauthorized", 403

@app.route("/")
def home():
    return "Webhook online", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


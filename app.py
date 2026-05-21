from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "juliana_webhook_2026"


@app.route("/", methods=["GET"])
def home():
    return "Assistente WhatsApp Juliana está online!", 200


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Erro de verificação", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Mensagem recebida:", data)
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

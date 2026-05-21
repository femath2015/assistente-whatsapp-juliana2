from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "juliana_webhook_2026"

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


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

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_number = message["from"]

        if "text" in message:
            user_text = message["text"]["body"]
            print("Texto recebido:", user_text)

            resposta = "Oi! Recebi sua mensagem. Sou o assistente da Juliana em fase de teste."

            enviar_mensagem_whatsapp(user_number, resposta)

    except Exception as e:
        print("Erro ao processar mensagem:", e)

    return "ok", 200


def enviar_mensagem_whatsapp(numero, texto):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status do envio:", response.status_code)
    print("Resposta da Meta:", response.text)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

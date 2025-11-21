from flask import Flask, request, jsonify, render_template
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# WhatsApp → Meta API → ngrok → Flask Webhook → LLaMA (local) → Flask → Meta API → WhatsApp

##############################################################################################################################

def fix_grammar(text):
    payload = {
        "model": "llama3.2",
        "prompt": (
            "Fix only grammar, punctuation, and sentence structure without changing "
            "the meaning. Do NOT add new content.\n\n"
            f"Input: {text}\n\nCorrected:"
        ),
        "stream": False
    }

    try:
        r = requests.post(app.config["LLAMA_API_URL"], json=payload)
        r.raise_for_status()


        data = r.json()
        print("LLaMA RAW OUTPUT:", data)

        # Try different keys based on Ollama output format
        if "response" in data:
            return data["response"].strip()
        if "output" in data:
            return data["output"].strip()

        return text
    except Exception as e:
        print("LLaMA error:", e)
        return text


##############################################################################################################################


def send_whatsapp_message(to_number, text):
    url = f"https://graph.facebook.com/v18.0/{app.config['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {app.config['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": text}
    }

    r = requests.post(url, json=payload, headers=headers)
    
    # Add logging
    print("WhatsApp Send Status:", r.status_code)
    print("WhatsApp Response:", r.text)


##############################################################################################################################


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/fix")
def api_fix():
    text = request.json.get("text", "")
    corrected = fix_grammar(text)
    return {"corrected": corrected}

##############################################################################################################################

@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == app.config["WHATSAPP_VERIFY_TOKEN"]:
        return challenge, 200

    return "Forbidden", 403


##############################################################################################################################

@app.post("/webhook")
def webhook():
    body = request.get_json()
    print(body)

    try:
        msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"]

        corrected = fix_grammar(text)

        # Forward to default receiver OR reply to sender
        target = app.config["DEFAULT_FORWARD_NUMBER"] or sender
        send_whatsapp_message(target, corrected)

    except Exception as e:
        print("Webhook error:", e)

    return "OK", 200

##############################################################################################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"])

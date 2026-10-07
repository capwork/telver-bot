import json
import os
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")


def send_message(chat_id: int, text: str) -> dict:
    """Send a text message through Telegram's Bot API."""
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def handler(request):
    """Vercel Python function receiving Telegram webhook updates."""
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "text/plain"},
            "body": "Method Not Allowed",
        }

    if WEBHOOK_SECRET:
        received_secret = request.headers.get(
            "x-telegram-bot-api-secret-token"
        )
        if received_secret != WEBHOOK_SECRET:
            return {
                "statusCode": 403,
                "headers": {"Content-Type": "text/plain"},
                "body": "Forbidden",
            }

    try:
        raw_body = request.body

        if isinstance(raw_body, bytes):
            raw_body = raw_body.decode("utf-8")

        update = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        message = update.get("message")
        if not message:
            return {"statusCode": 200, "body": "OK"}

        user_message = message.get("text")
        if not user_message:
            return {"statusCode": 200, "body": "OK"}

        chat_id = message["chat"]["id"]

        timestamp = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")

        response_text = (
            f"[{timestamp} IST]\n"
            f"You said: {user_message}"
        )

        send_message(chat_id, response_text)

        return {"statusCode": 200, "body": "OK"}

    except Exception as exc:
        print(f"Webhook error: {exc}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/plain"},
            "body": "Internal Server Error",
        }

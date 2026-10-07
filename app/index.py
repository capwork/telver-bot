import json
import os
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from zoneinfo import ZoneInfo


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")


def send_message(chat_id: int, text: str):
    """Send a message using Telegram Bot API."""

    if not BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN environment variable is missing"
        )

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    payload = json.dumps({
        "chat_id": chat_id,
        "text": text
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(
        request,
        timeout=15
    ) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        # -------------------------------
        # 1. Verify Telegram secret
        # -------------------------------

        if WEBHOOK_SECRET:

            received_secret = self.headers.get(
                "X-Telegram-Bot-Api-Secret-Token"
            )

            if received_secret != WEBHOOK_SECRET:

                self.send_response(403)
                self.end_headers()
                self.wfile.write(
                    b"Forbidden"
                )
                return

        # -------------------------------
        # 2. Read request body
        # -------------------------------

        content_length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        body = self.rfile.read(
            content_length
        )

        # -------------------------------
        # 3. Parse Telegram update
        # -------------------------------

        try:

            update = json.loads(
                body.decode("utf-8")
            )

        except json.JSONDecodeError:

            self.send_response(400)
            self.end_headers()
            self.wfile.write(
                b"Invalid JSON"
            )
            return

        # -------------------------------
        # 4. Get message
        # -------------------------------

        message = update.get("message")

        if not message:

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"OK"
            )
            return

        # -------------------------------
        # 5. Get user text
        # -------------------------------

        user_message = message.get("text")

        if not user_message:

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"OK"
            )
            return

        # -------------------------------
        # 6. Get chat ID
        # -------------------------------

        chat_id = message["chat"]["id"]

        # -------------------------------
        # 7. Generate timestamp
        # -------------------------------

        timestamp = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # -------------------------------
        # 8. Create response
        # -------------------------------

        response_text = (
            f"[{timestamp} IST]\n"
            f"You said: {user_message}"
        )

        # -------------------------------
        # 9. Send response to Telegram
        # -------------------------------

        try:

            send_message(
                chat_id,
                response_text
            )

        except Exception as error:

            print(
                f"Telegram API error: {error}"
            )

            self.send_response(500)
            self.end_headers()
            self.wfile.write(
                b"Telegram API error"
            )
            return

        # -------------------------------
        # 10. Return success to Telegram
        # -------------------------------

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()

        self.wfile.write(
            b"OK"
        )

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()

        self.wfile.write(
            b"Telegram bot webhook is running."
        )

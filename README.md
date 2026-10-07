# Telegram Echo Bot — Vercel Webhook

A minimal Telegram bot deployed as a Vercel Python serverless function.

It echoes every text message with an India (Asia/Kolkata) timestamp.

## Architecture

Telegram User
→ Telegram Servers
→ Vercel `/api/webhook`
→ `api/webhook.py`
→ Telegram Bot API `sendMessage`
→ User

This project uses Telegram webhooks, not polling.

## Project structure

```text
telegram-vercel-bot/
├── api/
│   └── webhook.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── vercel.json
```

## 1. Create the Telegram bot

In Telegram, open `@BotFather`:

```text
/start
/newbot
```

Choose a name and username. BotFather will give you a bot token.

Keep the token private.

## 2. Push this project to GitHub

Create a new GitHub repository, then from this folder:

```bash
git init
git add .
git commit -m "Initial Telegram Vercel bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Do not commit `.env`.

## 3. Deploy to Vercel

Import the GitHub repository into Vercel.

No build command is required for this simple project.

## 4. Add environment variables

In Vercel:

Project → Settings → Environment Variables

Add:

```text
TELEGRAM_BOT_TOKEN=your_real_bot_token
TELEGRAM_WEBHOOK_SECRET=your_random_secret
```

Redeploy after adding or changing environment variables if necessary.

## 5. Find your webhook URL

If Vercel gives you:

```text
https://telegram-vercel-bot.vercel.app
```

your webhook endpoint is:

```text
https://telegram-vercel-bot.vercel.app/api/webhook
```

## 6. Register the webhook

Open this URL in a browser or call it with curl:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://YOUR_PROJECT.vercel.app/api/webhook&secret_token=YOUR_WEBHOOK_SECRET
```

For example:

```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
  -d "url=https://YOUR_PROJECT.vercel.app/api/webhook" \
  -d "secret_token=YOUR_WEBHOOK_SECRET"
```

Telegram should return:

```json
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

## 7. Test

Open your bot in Telegram and send:

```text
Hello
```

Expected response:

```text
[2026-10-07 16:00:00 IST]
You said: Hello
```

## Check webhook status

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo
```

## Remove webhook

If you want to switch back to polling later:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/deleteWebhook
```

## Security

- Never commit `.env` or expose your bot token.
- Keep `TELEGRAM_WEBHOOK_SECRET` private.
- The webhook function checks the `X-Telegram-Bot-Api-Secret-Token` header when a secret is configured.
- If a bot token is accidentally exposed, regenerate it through BotFather.

## Important

The bot currently handles only text messages. Images, documents, stickers, commands, callback queries, and other Telegram update types are intentionally ignored.

The next natural extension is to replace the echo response with an LLM call while keeping the same webhook pipeline.

# ST FF API Bot — external Telegram server

InfinityFree free hosting blocks Telegram API traffic and webhooks, so the bot backend must run on a host that permits outbound Telegram API requests.

## Deploy on Render

1. Put this folder in a GitHub repository.
2. In Render, create a new **Web Service** from the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 60`
5. Add environment variables:
   - `BOT_TOKEN` = your NEW token from BotFather
   - `WEBHOOK_SECRET` = any long random string
6. After deployment, open:
   `https://YOUR-RENDER-DOMAIN/set-webhook`
7. Open:
   `https://YOUR-RENDER-DOMAIN/webhook-info`
   and confirm the webhook URL ends with `/webhook`.
8. Send `/start` to the bot.

## Important

The token that was previously exposed in chat should be revoked/regenerated in BotFather before deployment. Never commit the token to GitHub.

The `/check` command is intentionally a shell only. A legitimate/public Free Fire player-data source still needs to be configured for real UID -> name lookup.

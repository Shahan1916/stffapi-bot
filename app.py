import os
import re
import logging
from flask import Flask, request
import requests

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
TOKEN = os.environ.get('BOT_TOKEN', '').strip()
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '').strip()

if not TOKEN:
    logging.warning('BOT_TOKEN is not configured')

TG = f'https://api.telegram.org/bot{TOKEN}'

def telegram(method, data):
    if not TOKEN:
        raise RuntimeError('BOT_TOKEN is not configured')
    r = requests.post(f'{TG}/{method}', data=data, timeout=20)
    r.raise_for_status()
    return r.json()

def send_message(chat_id, text):
    return telegram('sendMessage', {'chat_id': chat_id, 'text': text})

@app.get('/')
def home():
    return {'ok': True, 'service': 'ST FF API Bot'}

@app.get('/health')
def health():
    return {'ok': bool(TOKEN)}

@app.post('/webhook')
def webhook():
    if WEBHOOK_SECRET and request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET:
        return 'forbidden', 403
    update = request.get_json(silent=True) or {}
    msg = update.get('message') or {}
    chat_id = (msg.get('chat') or {}).get('id')
    text = (msg.get('text') or '').strip()
    if not chat_id:
        return 'OK'

    try:
        if text in ('/start', '/start@stffapi_bot'):
            send_message(chat_id, '✅ ST FF API Bot is online!\n\nSend: /check UID\nExample: /check 3067820239')
        elif re.fullmatch(r'/check(?:@\w+)?\s+\d{5,15}', text):
            uid = re.fullmatch(r'/check(?:@\w+)?\s+(\d{5,15})', text).group(1)
            send_message(chat_id, f'UID: {uid}\n\nLookup engine is ready, but no legitimate player-data source is configured yet.')
        else:
            send_message(chat_id, 'Use:\n/check UID\n\nExample:\n/check 3067820239')
    except Exception:
        logging.exception('Telegram send failed')
        # Return 200 so Telegram does not repeatedly retry a permanently failing update.
    return 'OK'

@app.get('/set-webhook')
def set_webhook():
    base = request.url_root.rstrip('/')
    secret = WEBHOOK_SECRET
    data = {'url': base + '/webhook'}
    if secret:
        data['secret_token'] = secret
    try:
        return telegram('setWebhook', data)
    except Exception as e:
        return {'ok': False, 'error': str(e)}, 500

@app.get('/webhook-info')
def webhook_info():
    try:
        return telegram('getWebhookInfo', {})
    except Exception as e:
        return {'ok': False, 'error': str(e)}, 500

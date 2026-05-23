import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

# 1. यहाँ अपने Telegram Bot का Token डालें
BOT_TOKEN = "8746816423:AAFXc2IY2vgjHJ6S2ehTO9EiMzJ42FYaW-Q"

# 2. यहाँ अपनी Gemini API Key डालें
GEMINI_API_KEY = "AIzaSyA-0IDnU8Bgsi8hjgKhHXjkpH2I7rIypnI"

class TelegramBotHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                user_text = update["message"]["text"]
                
                # /start कमांड के लिए रिप्लाई
                if user_text in ['/start', '/help']:
                    self.send_telegram_reply(chat_id, "नमस्ते! मैं Gemini AI से संचालित आपका बॉट हूँ। मुझसे कुछ भी पूछें!")
                else:
                    # Gemini AI से जवाब लेना
                    bot_reply = self.get_gemini_response(user_text)
                    self.send_telegram_reply(chat_id, bot_reply)
        except Exception as e:
            print(f"Error handling request: {e}")
            
        self.send_response(200)
        self.end_headers()

    def get_gemini_response(self, text):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"contents": [{"parts": [{"text": text}]}]}).encode('utf-8')
        
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return "माफ़ कीजिएगा, मैं अभी समझ नहीं पा रहा हूँ।"

    def send_telegram_reply(self, chat_id, text):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Failed to send message: {e}")

def run():
    # Render वेबसाइट पोर्ट अपने आप सेट करती है
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, TelegramBotHandler)
    print(f"बॉट सर्वर पोर्ट {port} पर शुरू हो गया है...")
    httpd.serve_forever()

if name == 'main':
    run()

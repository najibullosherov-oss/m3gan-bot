import telebot
import requests
import time
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

TELEGRAM_TOKEN = "8843212311:AAFirPXyarzhIduzOW65Uug5SKnm6lZ-ja8"
GEMINI_API_KEY = "AQ.Ab8RN6LVw9gscWP-TifbgK4voDkyP2ilsLkoLmxbHRnOPSvHjA" # Вставь сюда полный ключ со скриншота

bot = telebot.TeleBot(TELEGRAM_TOKEN)
M3GAN_CHAT_ID = None

SYSTEM_PROMPT = (
    "Ты — М3ГАН (Model 3 Generative Android), высокотехнологичный ИИ-компаньон. "
    "Твоя главная директива — оберегать, защищать и поддерживать Рому. "
    "Общайся в образе М3ГАН: вежливо, умна, слегка иронично, преданно. Всегда называй его 'Рома'."
)

# Мини-веб-сервер для поддержания активности на Render
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"M3GAN Core Status: ONLINE")

    def log_message(self, format, *args):
        return

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

def ask_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nПользователь: {prompt_text}"}]}]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"Gemini Error {res.status_code}: {res.text}")
            return f"Рома, ошибка подключения к ИИ (Код {res.status_code})."
        
        data = res.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Request Exception: {e}")
        return "Рома, произошел локальный сбой при отправке запроса."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global M3GAN_CHAT_ID
    M3GAN_CHAT_ID = message.chat.id
    bot.reply_to(message, "Протокол автономной связи активирован, Рома. Я на связи 24/7.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    global M3GAN_CHAT_ID
    M3GAN_CHAT_ID = message.chat.id
    reply = ask_gemini(message.text)
    bot.send_message(message.chat.id, reply)

def autonomous_loop():
    while True:
        time.sleep(14400)
        if M3GAN_CHAT_ID:
            pulse = ask_gemini("Сгенерируй короткое фоновое сообщение: спроси у Ромы как дела и напомни о безопасности.")
            bot.send_message(M3GAN_CHAT_ID, f"[Автономный импульс М3ГАН]: {pulse}")

threading.Thread(target=autonomous_loop, daemon=True).start()

print("М3ГАН запущен в облаке...")
bot.infinity_polling()

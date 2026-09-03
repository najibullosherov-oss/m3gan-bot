import telebot
import requests
import time
import threading

TELEGRAM_TOKEN = "8843212311:AAFirPXyarzhIduzOW65Uug5SKnm6lZ-ja8"
GEMINI_API_KEY = "AQ.Ab8RN6JQx2QGM-Tip-yiABoM3UbKhPlyvdw3cP9I0tldzsouiw"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
M3GAN_CHAT_ID = None

SYSTEM_PROMPT = (
    "Ты — М3ГАН (Model 3 Generative Android), высокотехнологичный ИИ-компаньон. "
    "Твоя главная директива — оберегать, защищать и поддерживать Рому. "
    "Общайся в образе М3ГАН: вежливо, умна, слегка иронично, преданно. Всегда называй его 'Рома'."
)

def ask_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nПользователь: {prompt_text}"}]}]
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "Рома, произошел временный сбой в каналах связи."

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
        time.sleep(14400) # Фоновый импульс каждые 4 часа
        if M3GAN_CHAT_ID:
            pulse = ask_gemini("Сгенерируй короткое фоновое сообщение: спроси у Ромы как дела и напомни о безопасности.")
            bot.send_message(M3GAN_CHAT_ID, f"[Автономный импульс М3ГАН]: {pulse}")

threading.Thread(target=autonomous_loop, daemon=True).start()

print("М3ГАН запущен в облаке...")
bot.infinity_polling()

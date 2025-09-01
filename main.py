import telebot
import requests
import json
from flask import Flask, request

TELEGRAM_TOKEN = "8353978400:AAGTWnBSvz3KIfkJAUegpBWjurL_PBvmBhM"
OPENWEATHER_API = "e9ed9cc83a633d513fc8fd7acbd2a24b"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города на английском языке')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API}&units=metric&lang=ru')
    data = json.loads(res.text)

    if data.get("cod") != "200":
        bot.send_message(message.chat.id, "❌ Город не найден. Напиши название города на английском языке")
        return

    temp = round(data['list'][0]['main']['temp'])
    description = data['list'][0]['weather'][0]['main'].lower()

    if 'clear' in description:
        label = "Солнечно"
        photo_path = 'images/Солнечно.jpg'
    elif 'cloud' in description:
        label = "Облачно"
        photo_path = 'images/Облачно.jpg'
    elif 'rain' in description and 'thunder' in description:
        label = "Местами грозы"
        photo_path = 'images/Местами Грозы.jpg'
    elif 'rain' in description:
        label = "Дождь"
        photo_path = 'images/Дождь.jpg'
    elif 'snow' in description:
        label = "Снег"
        photo_path = 'images/Снег.jpg'
    else:
        label = "Туманно"
        photo_path = 'images/Туманно.jpg'

    if temp > 25:
        thermometer = "🔥🌡️"
    elif temp < 0:
        thermometer = "❄️🌡️"
    else:
        thermometer = "🌡️"

    with open(photo_path, "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f"{label}\nТемпература: {temp}°C {thermometer}"
        )

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def webhook():
    update = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "!", 200

@app.route('/')
def index():
    return "Бот работает"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://openweather365.onrender.com/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=5000)




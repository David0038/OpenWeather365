from flask import Flask
import threading
import telebot
import requests
import json
import os

app = Flask(__name__)

TELEGRAM_TOKEN = 'твоя строка токена'
OPENWEATHER_API = 'твоя строка API'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric&lang=ru')
    data = json.loads(res.text)
    temp = data['main']['temp']
    description = data['weather'][0]['main'].lower()

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

def run_bot():
    bot.polling(none_stop=True)

threading.Thread(target=run_bot).start()

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

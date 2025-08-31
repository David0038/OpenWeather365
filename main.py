import telebot
import requests
import json

bot = telebot.TeleBot('8353978400:AAGTWnBSvz3KIfkJAUegpBWjurL_PBvmBhM')
API = 'e9ed9cc83a633d513fc8fd7acbd2a24b'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет рад тебя видеть! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')
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


bot.polling(none_stop=True)


import os

from dotenv import load_dotenv
import telebot
from pyowm import OWM


load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)
    text: str = message.text
    if text.startswith('/weather') and text.rstrip() != '/weather':
        get_weather(message)
    elif text.startswith('/weather'):
        bot.send_message(message.chat.id, 'Напиши: /weather Пермь')


def get_location(lat, lon):
    url = f"https://yandex.ru/pogoda/maps/nowcast&lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url


def weather(city: str):
    owm = OWM(os.getenv('OWM_TOKEN'))
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    city_weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = city_weather.temperature("celsius")
    return temperature, location


def get_weather(message):
    command, city = message.text.split()
    print(city)
    try:
        w = weather(city)
        print(w[1])
        bot.send_message(
            message.chat.id,
            f"В городе {city} сейчас {round(w[0]['temp'])} градусов, "
            f"чувствуется как {round(w[0]['feels_like'])} градусов."
        )
        bot.send_message(message.chat.id, f'{w[1]}')
    except Exception as e:
        print(e)
        bot.send_message(
            message.chat.id,
            'Упс... такого города нет в базе, попробуйте ещё раз.'
        )


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()

import logging
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO, encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
token, Api_key, url_weather_api = ('7460813472:AAFsTLMO2jVbMohR3SFHMfkU__HoZyi6Uu0', '08dd0246241daa84a2047467225e2613',
                                   'https://api.openweathermap.org/data/2.5/weather')
EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀️',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}
bot = telebot.TeleBot(token)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))


def get_weather(lat, lon):
    logging.info('Запрос к API и возврат строки с ответом')
    params = {'lat': lat, 'lon': lon, 'lang': 'ru', 'units': 'metric', 'appid': Api_key}
    response = requests.get(url=url_weather_api, params=params).json()
    city = response['name']
    desc = response['weather'][0]['description']
    temp = response['main']['temp']
    temp_feel = response['main']['feels_like']
    hum = response['main']['humidity']
    code = response['weather'][0]['id']
    return f'🏙Погода в: {city}\n{EMOJI_CODE[code]}{desc.capitalize()}\n🌡Температура: {temp}\n🌡Ощущается как: {temp_feel}\n💧Влажность: {hum}'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info('Приветствие')
    bot.send_message(message.chat.id, 'Привет! Отправь мне своё местоположение и я отправлю тебе погоду',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    logging.info('Извлечение координат и отправка ответа')
    lon, lat = message.location.longitude, message.location.latitude
    weather = get_weather(lat, lon)
    bot.send_message(message.chat.id, weather)


@bot.message_handler(regexp='О проекте')
def send_about(message):
    logging.info('Сообщение о проекте')
    bot.send_message(message.chat.id, '')


bot.infinity_polling()

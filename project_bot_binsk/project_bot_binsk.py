import telebot
from setting import valid_token_bs

from telebot import types
import random

import requests
import json
from api import *


bot = telebot.TeleBot(valid_token_bs)


@bot.message_handler(commands=['biysk'])
def get_weather(message):
    r = requests.get(url=url_1, headers=headers)
    # bot.send_message(message.chat.id, r.text)
    if r.status_code == 200:
        # получаем значение погоды
        data = json.loads(r.text)
        # Объекты fact
        fact = data["fact"]
        # Код расшифровки погодного описания. В api.py созданы ключи
        weather_description = data["fact"]["condition"]
        if weather_description in condition:
            wd = condition[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Посмотри в окно, я не понимаю, что там за погода..."
        # Объекты forecast
        forecast = data["forecast"]
        # url для большого прогноза из Объектов info
        url = data["info"]
        bot.send_message(message.chat.id, text=f'Температура в Бийске {fact["temp"]}°. '
                                               f'\nОщущается как {fact["feels_like"]}°. '
                                               f'\nСейчас на улице {wd}.'
                                               f'\nДавление {fact["pressure_mm"]} мм рт.ст.'
                                               f'\nВлажность воздуха {fact["humidity"]} %.'
                                               f'\nСкорость ветра {fact["wind_speed"]} м\с.'
                                               f'\nРассвет {forecast["sunrise"]}.'
                                               f'\nЗакат{forecast["sunset"]}.'
                                               f'\nПодробный прогноз на несколько дней {url["url"]}.')
    else:
        bot.send_message(message.chat.id, 'Problems on weather API')


@bot.message_handler(commands=['krasnoobsk'])
def get_weather(message):
    r = requests.get(url=url_2, headers=headers)
    # bot.send_message(message.chat.id, r.text)
    if r.status_code == 200:
        # получаем значение погоды
        data = json.loads(r.text)
        # Объекты fact
        fact = data["fact"]
        # Код расшифровки погодного описания. В api.py созданы ключи
        weather_description = data["fact"]["condition"]
        if weather_description in condition:
            wd = condition[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Посмотри в окно, я не понимаю, что там за погода..."
        # Объекты forecast
        forecast = data["forecast"]
        # url для большого прогноза из Объектов info
        url = data["info"]
        bot.send_message(message.chat.id, text=f'Погода в Краснообске {fact["temp"]}°, '
                                               f'\nОщущается как {fact["feels_like"]}°. '
                                               f'\nСейчас на улице {wd}.'
                                               f'\nДавление {fact["pressure_mm"]} мм рт.ст.'
                                               f'\nВлажность воздуха {fact["humidity"]} %.'
                                               f'\nСкорость ветра {fact["wind_speed"]} м\с.'
                                               f'\nРассвет {forecast["sunrise"]}.'
                                               f'\nЗакат{forecast["sunset"]}.'
                                               f'\nПодробный прогноз на несколько дней {url["url"]}.')
    else:
        bot.send_message(message.chat.id, 'Problems on weather API')


@bot.message_handler(commands=['love'])
def send_welcome(message: telebot.types.Message):
    print(message.text)  # выводит текст в консоль
    # bot.reply_to(message, f"Пожелание Божиих благословений")
    bot.send_message(message.chat.id, f"Как же я люблю тебя, дорогушечка {message.from_user.first_name}")


@bot.message_handler(content_types=['voice'])
def function_name(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Ну какой же у тебя шикарный голос")


@bot.message_handler(content_types=['photo'])
def answer_on_photo(message: telebot.types.Message):
    if message.from_user.first_name == 'Татьяна':
        bot.send_message(message.chat.id, 'Какая милота')
    else:
        pass


# Загружаем список интересных фактов
f = open('facts.txt', 'r', encoding='UTF-8')
facts = f.read().split('\n')
f.close()
# Загружаем список поговорок
f = open('thinks.txt', 'r', encoding='UTF-8')
thinks = f.read().split('\n')
f.close()

# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода")
    item2 = types.KeyboardButton("Факт")
    item3 = types.KeyboardButton("Поговорка")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(m.chat.id, 'Нажми: '
                                '\nКнопочку "Погода" чтобы посмотреть погоду '
                                '\nКнопочку "Факт" для получения интересного факта'
                                '\n Кнопочку "Поговорка" — для получения мудрой цитаты ',
                     reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер нажал ФАКТ, выдаем ему случайный факт
    if message.text.strip() == 'Факт':
        answer = random.choice(facts)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, answer)
    # Если юзер нажал Поговорка, выдаем умную мысль
    elif message.text.strip() == 'Поговорка':
        answer = random.choice(thinks)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Погода':
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                          f'Я могу показать тебе погоду в: \n/biysk \n/krasnoobsk')
    elif 'Саша' in message.text.strip():
        bot.send_message(message.chat.id, 'Саша, самый лучший во всем мире')
    elif 'деньги' in message.text.strip():
        bot.send_message(message.chat.id, f'Контакт {message.from_user.first_name} '
                                          f'заблокирован на 30 лет, 3 месяца и 12 дней')
    else:
        pass


# Запускаем бота
bot.polling(none_stop=True)  # чтобы запустить бота
# параметр none_stop=True говорит, что бот должен стараться не прекращать работу
# при возникновении каких-либо ошибок


import telebot
from settings import valid_token_bs
# from telebot import types
import random
import requests
import json
from api import *
import os

bot = telebot.TeleBot(valid_token_bs)

# @bot.callback_query_handler(func=lambda call: call.data == 'biysk')
# def save_btn(call):

# Погода в двух населенных пунктам
@bot.message_handler(commands=['biysk', 'krasnoobsk'])
def get_weather(message):
    # тернарный условный оператор
    city = 'Бийскe' if 'biysk' in message.text else 'Краснообске'  # изменяемые данные
    url_loc = url_bs if 'biysk' in message.text else url_ks  # изменяемые данные

    # global url_loc, city
    # if 'biysk' in message.text:
    #     city, url_loc = 'Бийскe', url_bs  # изменяемые данные
    # elif 'krasnoobsk' in message.text:
    #     city, url_loc = 'Краснообске', url_ks  # изменяемые данные
    # else:
    #     pass
    r = requests.get(url=base_url + url_loc, headers=headers)
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
        bot.send_message(message.chat.id, text=f'Температура в {city} {fact["temp"]}°. '
                                               f'\nОщущается как {fact["feels_like"]}°. '
                                               f'\nСейчас на улице {wd}.'
                                               f'\nДавление {fact["pressure_mm"]} мм рт.ст.'
                                               f'\nВлажность воздуха {fact["humidity"]} %.'
                                               f'\nСкорость ветра {fact["wind_speed"]} м/с.'
                                               f'\nРассвет {forecast["sunrise"]}.'
                                               f'\nЗакат{forecast["sunset"]}.'
                                               f'\nПодробный прогноз на несколько дней {url["url"]}.')
    else:
        bot.send_message(message.chat.id, 'Problems on weather API')

# Признание
@bot.message_handler(commands=['love'])
def send_love(message: telebot.types.Message):
    print(message.text)  # выводит текст в консоль
    bot.send_message(message.chat.id,
                     f"Как же я люблю тебя, хорошего тебе дня {message.from_user.first_name}")

# Реакция на голосовое сообщение
@bot.message_handler(content_types=['voice'])
def function_voice(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Ну какой же у тебя шикарный голос")


# Оценка фото от Татьяны
@bot.message_handler(content_types=['photo', 'sticker', 'gif'])
def answer_on_photo(message: telebot.types.Message):
    if message.from_user.first_name == 'Татьяна':
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, какая милота!")  # сообщение с
        # привязкой к пользователю
        # bot.reply_to(message, 'Какая милота!')  # # сообщение с привязкой к картинке.
    else:
        pass

# реакция бота на загружаемые видео
@bot.message_handler(content_types=['video'])
def answer_on_photo(message: telebot.types.Message):
    # эмоджи - огонь
    emoji = "\U0001f525"
    # берет рандомный ответ из файла answers.txt
    answer = random.choice(answers)
    # Отсылаем юзеру сообщение в чат
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, хоть я и бот, но {answer}'
                                      f'{emoji}')

# Команда start
# Кнопки
@bot.message_handler(commands=['start'])
def start(message, res=False):
    # Добавляем три кнопки
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)  # клавиатура
    button1 = telebot.types.KeyboardButton(text='Погода')
    button2 = telebot.types.KeyboardButton(text='Факт')
    button3 = telebot.types.KeyboardButton(text='Поговорка')
    keyboard.add(button1)  # одна кнопка в ряду
    keyboard.add(button2, button3)  # две кнопки в ряду
    # bot.send_message(message.chat.id, 'Нажми: '
    #                                       '\nКнопочку "Погода" чтобы посмотреть погоду '
    #                                       '\nКнопочку "Факт" для получения интересного факта'
    #                                       '\nКнопочку "Поговорка" — для получения мудрой цитаты ',
    #                                       # '\nМожешь и музыку послушать',
    #                      reply_markup=keyboard)
    # audio = open(r'Zivert_Life.mp3', 'rb')
    # bot.send_audio(message.chat.id, audio)
    # audio.close()


# Реакция бота на сообщение от юзера
@bot.message_handler(content_types=['text'])
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
        # keyboard = telebot.types.InlineKeyboardMarkup()  # клавиатура
        # button_1 = telebot.types.InlineKeyboardButton(text='Бийск', callback_data='biysk')
        # button_2 = telebot.types.InlineKeyboardButton(text='Краснообск', callback_data='krasnoobsk')
        # keyboard.add(button_1, button_2)
        # bot.send_message(message.chat.id,
        #                  f'{message.from_user.first_name}!\n Я могу показать тебе погоду в:',
        #                  reply_markup=keyboard)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, f'{message.from_user.first_name}!\n'
                                          f'Я могу показать тебе погоду в: \n/biysk \n/krasnoobsk')

    # elif 'деньги' in message.text.strip():
    #     bot.send_message(message.chat.id, f'Контакт {message.from_user.first_name} '
    #                                       f'заблокирован на 30 лет, 3 месяца и 12 дней')
    else:
        pass

# Загружаем список интересных фактов
way_facts = os.path.join('project_bot_binsk', 'facts.txt')
with open(way_facts, 'rt', encoding='UTF8') as f:
    facts = f.read().split('\n')
# Загружаем список поговорок
way_thinks = os.path.join('project_bot_binsk', 'thinks.txt')
with open(way_thinks, 'rt', encoding='UTF8') as f:
    thinks = f.read().split('\n')
# Загружаем список ответов на загруженное видео
way_answers = os.path.join('project_bot_binsk', 'answers.txt')
with open(way_answers, 'rt', encoding='UTF8') as f:
    answers = f.read().split('\n')



# Запускаем бота
# bot.infinity_polling(none_stop=True)
bot.polling(none_stop=True)  # чтобы запустить бота
# параметр none_stop=True говорит, что бот должен стараться не прекращать работу
# при возникновении каких-либо ошибок


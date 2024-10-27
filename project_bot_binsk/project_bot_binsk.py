import telebot
import random
import requests
import json

from telebot.types import InlineKeyboardMarkup

from settings import valid_token_bs
from api import *
from files import *

# подгружаем бота
bot = telebot.TeleBot(valid_token_bs)


# Команда start
# Кнопки *Погода *Факт *Поговорка
@bot.message_handler(commands=['start'])
def start(message, res=False):
    # Добавляем четыре кнопки
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)  # клавиатура
    # resize_keyboard=True для нормальной работы кнопок, в некоторых случаях кнопки могут сильно растягиваться
    button1 = telebot.types.KeyboardButton(text='Погода')
    button2 = telebot.types.KeyboardButton(text='Факт')
    button3 = telebot.types.KeyboardButton(text='Анекдот')
    button4 = telebot.types.KeyboardButton(text='Поговорка')
    keyboard.add(button1)  # одна кнопка в ряду
    keyboard.add(button2, button3, button4)  # три кнопки в ряду
    # эмодзи - '😘'
    emoji = "\U0001f618"
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, чмоки, \nчмоки, {emoji}!',
                     reply_markup=keyboard)


# Реакция бота на сообщение от юзера
@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Если юзер нажал Факт, выдаем ему случайный факт
    if message.text.strip() == 'Факт':
        # strip() - функция используется для удаления символов или пробелов из начала и конца исходной строки.
        answer = random.choice(facts)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, answer)
    # Если юзер нажал Поговорка, выдаем умную мысль
    elif message.text.strip() == 'Поговорка':
        answer = random.choice(thinks)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, answer)
    # Если юзер нажал Погода, выдаем текст с предложением о выборе погоды и две кнопки: *погода в Бийске,
    # *погода в Краснообске
    # Если юзер нажал Анекдот, выдаем случайный анекдот
    elif message.text.strip() == 'Анекдот':
        answer_anecdote = random.choices(anecdote)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, answer_anecdote)
    elif message.text.strip() == 'Погода':
        keyboard_weather = telebot.types.InlineKeyboardMarkup(row_width=2)  # InlineKeyboardMarkup - для
        # использования клавиатуры Inline # row_width=2 - две кнопки
        button_1 = telebot.types.InlineKeyboardButton(text='Бийск', callback_data='biysk')  # callback_data
        # - параметр, переносимый в функцию def callback_inline(call): При нажатии никакого сообщения не
        # отправляется, а сервер телеги отправляет запрос боту, что была нажата кнопка, которая прописана в
        # callback_data
        button_2 = telebot.types.InlineKeyboardButton(text='Краснообск', callback_data='krasnoobsk')
        keyboard_weather.add(button_1, button_2)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, f'{message.from_user.first_name},\n'
                                          f'выбери, где хочешь узнать погоду!',
                         reply_markup=keyboard_weather)
        keyboard_news = telebot.types.InlineKeyboardMarkup(row_width=1)
        button_1 = telebot.types.InlineKeyboardButton(text='Новости', callback_data='news',
                                                      url='https://nsk.rbc.ru/')
        keyboard_news.add(button_1)
        bot.send_message(message.chat.id, f'Ты можешь также узнать последние новости с РБК- '
                                          f'Новосибирск',
                         reply_markup=keyboard_news)
    else:
        pass


# Погода в двух населенных пунктам
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # тернарный условный оператор
    city = 'Бийскe' if 'biysk' in call.data else 'Краснообске'  # изменяемые данные
    url_loc = url_bs if 'biysk' in call.data else url_ks  # изменяемые данные

    r = requests.get(url=base_url + url_loc, headers=headers)

    # если запрос проходит с кодом 200, то бот показывает погоду
    if r.status_code == 200:
        # получаем значение погоды с сайта
        data = json.loads(r.text)
        # Объекты fact
        fact = data["fact"]
        # код расшифровки погодного описания. В api.py созданы ключи
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
        bot.send_message(call.message.chat.id, text=f'Температура в {city} {fact["temp"]}°. '
                                                    f'\nОщущается как {fact["feels_like"]}°. '
                                                    f'\nСейчас на улице {wd}.'
                                                    f'\nДавление {fact["pressure_mm"]} мм рт.ст.'
                                                    f'\nВлажность воздуха {fact["humidity"]} %.'
                                                    f'\nСкорость ветра {fact["wind_speed"]} м/с.'
                                                    f'\nРассвет {forecast["sunrise"]}.'
                                                    f'\nЗакат{forecast["sunset"]}.'
                                                    f'\nПодробный прогноз на несколько дней {url["url"]}.')
    else:
        bot.send_message(call.message.chat.id, 'Блин, что-то на серваке сломалось')


# Реакция бота на голосовое сообщение
@bot.message_handler(content_types=['voice'])
def voice_message_bot(message: telebot.types.Message):
    bot.reply_to(message, f"{message.from_user.first_name}, ну какой же у тебя шикарный голос")  # ответ
    # бота, с привязкой к сообщению и к имени пользователя

# Реакция бота на стикеры
@bot.message_handler(content_types=['sticker'])
def sticker_message_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, вау! Ты умеешь пользоваться "
                                      f"стикерами?")  # ответ бота,
    # без привязки к сообщению, но с привязкой к имени пользователя

# Оценка ботом фото от Татьяны
@bot.message_handler(content_types=['photo'])  # ['photo', 'sticker', 'gif']
def photo_message_bot(message: telebot.types.Message):
    if message.from_user.first_name == 'Татьяна':
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, какая милота!")  # ответ бота,
        # без привязки к сообщению, но с привязкой к имени пользователя

# Реакция бота на загружаемые видео
@bot.message_handler(content_types=['video'])
def video_message_bot(message: telebot.types.Message):
    if not message.from_user.first_name == 'Захар':
        # эмодзи - '🔥'
        emoji = "\U0001f525"
        # берет рандомный ответ из файла answers.txt
        answer_video = random.choice(ans_video)
        # Отсылаем юзеру сообщение в чат
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, {answer_video}'
                                          f'{emoji}')


# Запускаем бота
# bot.polling(none_stop=True)
if __name__ == '__main__':
    print('Bot started!')
    bot.infinity_polling(none_stop=True)  # чтобы запустить бота
# параметр none_stop=True говорит, что бот должен стараться не прекращать работу при возникновении
# каких-либо ошибок
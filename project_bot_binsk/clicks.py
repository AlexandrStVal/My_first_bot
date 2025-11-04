from mysql.connector import connect, Error  #
from settings import password, database_name  #
import time

# # --- КОНФИГУРАЦИЯ БОТА ---
# MAX_PRESSES_PER_HOUR = 5  # Максимальное количество нажатий за интервал
# RESET_INTERVAL_SECONDS = 3600  # Интервал сброса счетчика (3600 секунд = 1 час)
# # ------------------------

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ ---
def create_connection(hostname, username):
    connection = None
    try:
        connection = connect(
            host=hostname,
            user=username,
            passwd=password,
            db=database_name
        )
        print("Connection to MySQL DB successful")
    except Error as err:
        print(f"The error '{err}' occurred")
    return connection

connect_db = create_connection("localhost", "root")

# def create_db(connect_db):
#     cursor = connect_db.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS user_limits (
#             user_id INTEGER PRIMARY KEY,
#             press_count INTEGER DEFAULT 0,
#             last_reset_time REAL DEFAULT 0.0
#         )
#     ''')
#     connect_db.commit()
#     connect_db.close()
#
# def get_user_limit_data(connect_db, user_id):
#     cursor = connect_db.cursor()
#     cursor.execute("SELECT press_count, last_reset_time FROM user_limits WHERE user_id = ?", (user_id,))
#     result = cursor.fetchone()
#     connect_db.close()
#     if result:
#         return {'count': result[0], 'last_reset_time': result[1]}
#     return None  # Пользователь не найден в базе
#
# def update_user_limit_data(connect_db, user_id, count, last_reset_time):
#     cursor = connect_db.cursor()
#     cursor.execute('''
#         INSERT OR REPLACE INTO user_limits (user_id, press_count, last_reset_time)
#         VALUES (?, ?, ?)
#     ''', (user_id, count, last_reset_time))
#     connect_db.commit()
#     connect_db.close()
# # ----------------------------------------
#
# # Инициализируем базу данных при запуске бота
# create_db(connect_db)
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     markup = types.InlineKeyboardMarkup()
#     btn = types.InlineKeyboardButton("Нажми меня!", callback_data="example_button_press")
#     markup.add(btn)
#     bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы что-то сделать. У меня есть ограничение на нажатия (с сохранением!).", reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: call.data == "example_button_press")
# def handle_button_press(call):
#     user_id = call.from_user.id
#     current_time = time.time()
#
#     # Получаем данные пользователя из БД
#     user_stats = get_user_limit_data(user_id)
#     if user_stats is None:
#         # Если пользователь новый, инициализируем его данные
#         user_stats = {'count': 0, 'last_reset_time': current_time}
#         update_user_limit_data(user_id, user_stats['count'], user_stats['last_reset_time'])
#
#     new_count = user_stats['count']
#     new_last_reset_time = user_stats['last_reset_time']
#     response_text = ""
#
#     # Проверяем, прошел ли интервал сброса
#     if current_time - user_stats['last_reset_time'] > RESET_INTERVAL_SECONDS:
#         # Если прошел, сбрасываем счетчик и обновляем время сброса
#         new_count = 1 # Это первое нажатие в новом интервале
#         new_last_reset_time = current_time
#         response_text = f"Вы нажали кнопку! Ваш счетчик сброшен. (1/{MAX_PRESSES_PER_HOUR})"
#     else:
#         # Если не прошел, увеличиваем счетчик
#         new_count += 1
#         if new_count > MAX_PRESSES_PER_HOUR:
#             # Если превышен лимит
#             bot.answer_callback_query(
#                 call.id,
#                 f"Вы достигли лимита в {MAX_PRESSES_PER_HOUR} нажатий в час. Попробуйте позже.",
#                 show_alert=True
#             )
#             return # Прекращаем обработку нажатия
#         response_text = f"Вы нажали кнопку! Нажатий: {new_count}/{MAX_PRESSES_PER_HOUR}"
#
#     # Обновляем данные пользователя в БД
#     update_user_limit_data(user_id, new_count, new_last_reset_time)
#
#     # Отправляем ответ пользователю
#     bot.answer_callback_query(call.id, response_text)
#     # bot.send_message(call.message.chat.id, response_text) # Опционально: отправить сообщение в чат
#
# # Запуск бота
# print("Бот запущен с persistent-хранилищем...")
# bot.polling(none_stop=True)
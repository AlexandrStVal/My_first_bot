import os
import csv
import datetime

# Загружаем список интересных фактов
way_facts = os.path.join('project_bot_binsk', 'facts.txt')
with open(way_facts, 'rt', encoding='UTF8') as f:
    facts = f.read().split('\n')

# Загружаем список поговорок
way_thinks = os.path.join('project_bot_binsk', 'thinks.txt')
with open(way_thinks, 'rt', encoding='UTF8') as f:
    thinks = f.read().split('\n')

# Загружаем список анекдотов
way_anecdotes = os.path.join('project_bot_binsk', 'anecdotes.txt')
with open(way_anecdotes, 'rt', encoding='UTF8') as f:
    anecdote = f.read().split('\n')

# Загружаем список ответов на видео
way_ans_video = os.path.join('project_bot_binsk', 'ans_video.txt')
with open(way_ans_video, 'rt', encoding='UTF8') as f:
    ans_video = f.read().split('\n')

# # Загружаем список важных дат
# way_imp_date = os.path.join('project_bot_binsk', 'imp_date.csv')
# with open(way_imp_date, 'r') as f:
#     csv_reader = csv.DictReader(f)
#     # csv_reader = csv.reader(f)
#     # Напоминание бота о важной дате
#     # Определение текущей даты
#     current_date = datetime.datetime.now().strftime('%Y-%m-%d')
#     # метод strftime(), который позволяет форматировать дату по заданной маске.
#     for row in csv_reader:
#         # Сравнение текущей даты с датой, в csv файле
#         print(row)
#         if current_date in row:
#             # если есть событие
#             even_dict.update(element)
#         if current_date not in row:
#         # если нет события
#             text_event = 'Сегодня нет праздников!'
#             break
#         print(even_dict)




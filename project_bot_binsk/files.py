import os

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


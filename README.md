Мой Ну очень начальный)) бот!  

Имя бота @BinskStBot

Настройка проекта:
1. Создаем виртуальное окружение командой:
    python -m venv venv
2. Активируем виртуальное окружение командой (MacOS/Linux):
    source venv/bin/activate
   для Windows другая команда:
    \env\Scripts\activate
3. Установка зависимостей:
    pip install -r requirements.txt
4. Настроить в IDE(Pycharm) текущий интерпритатор, выбрав текущее 
   виртуальное окружение  

Чтобы бот заработал нужно написать /start

Данный бот умеет:
1. При нажатии кнопки "Погода", говорить погоду в двух населенных пунктах 
   (но для этого нужно зарегистрироваться на API Яндекс. Погоды 
   https://yandex.ru/dev/weather/. Он бесплатный, но есть ограничение, 50 
   запросов в сутки). 
2. Оценивать голос.
3. Оценивать видео.
4. Оценивать фото (настроено на конкретного пользователя).
5. При нажатии кнопки "Факт" публиковать странные факты).
6. При нажатии кнопки "Поговорка" публиковать поговорки.

В директории project_bot_binsk:
* размещен файл api.py, содержащий urlы для запросов и обязательный headers  
* размещены файлы facts.txt (с рандомными фактами) и thinks.txt (c рандомными 
  поговорками).
* размещен файл files.py, содержащий ссылки на текстовые файлы. 
* размещен файл ans_video.txt, содержащий рандомные реакции на полученное 
  видео.
* размещен файл anecdotes.txt, содержащий анекдоты.

В корневой директории лежит файл:
* settings.py - содержит отсылку на файл .env, содержащий информацию о 
  токине бота и ключе для Яндекс Погоды. 
* .gitignore - содержит исключения для git'а.
* requirements.txt - библиотеки



# код для эмодзи
#s = '😘'
#print(s.encode('unicode-escape').decode('ASCII'))
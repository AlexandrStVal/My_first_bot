import os
from dotenv import load_dotenv

load_dotenv()  # функция из библиотеки python-dotenv, которая загружает переменные среды из файла
# .env в проект

# получение доступа к переменным среды с помощью функции os.getenv()
valid_token_ch = os.getenv('TOKEN_ch')
valid_token_bs = os.getenv('TOKEN_bs')
valid_key_ya = os.getenv('KEY_ya')
valid_token_conv = os.getenv('TOKEN')

# MySQL
password = os.getenv('password')
database_name = os.getenv('database_name')
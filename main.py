import os
import telebot
import logging
import sqlite3
from dotenv import load_dotenv

load_dotenv()
x = os.getenv("API_KEY")
bot = telebot.TeleBot(x)

conn = sqlite3.connect('db/database.db')
cursor = conn.cursor()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name) VALUES (?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    db_table_val(user_id=us_id, user_name=us_name)

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


# Команда /continue
@bot.message_handler(commands=['continue'])
def continue_quiz(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


# Команда /play начинает квест
@bot.message_handler(commands=['play'])
def play_quiz(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


# Команда /help
@bot.message_handler(commands=['help'])
def help_quiz(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


# Обработка ответов пользователя
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')


bot.polling()

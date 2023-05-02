import os
import telebot
import logging
from db import Database
import sqlite3
from dotenv import load_dotenv


load_dotenv()
x = os.getenv("API_KEY")
bot = telebot.TeleBot(x)
db = Database('database.db')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

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
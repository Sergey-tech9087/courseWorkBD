# -*- coding: utf-8 -*-
import telebot
import os
from telebot import types
import logging 
import requests 
import ast
from db import Database
import sqlite3
from dotenv import load_dotenv

load_dotenv()
 
API = os.getenv('API')

bot = telebot.TeleBot(API)
db = Database('database.db')

logging.basicConfig( 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO, 
) 
logger = logging.getLogger(__name__) 



# Команда /start
@bot.message_handler(commands=['start']) 
def start_quiz(message):
    bot.send_message(message.chat.id, "result")


bot.polling()
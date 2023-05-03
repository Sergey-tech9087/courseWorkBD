# -*- coding: utf-8 -*-
import telebot
from telebot import types
import logging 
import requests 
import ast
from db import Database
import sqlite3
 
bot = telebot.TeleBot("6196088116:AAEgf1DOhfBwDDrKoVX69n667BLa_oY9gEU")
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
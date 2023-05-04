# -*- coding: utf-8 -*-
import telebot
import os
from telebot import types
import logging 
import requests 
import ast
from db import Database
import sqlite3
import pickledb
from dotenv import load_dotenv

load_dotenv()
 
API = os.getenv('API')

bot = telebot.TeleBot(API)
db = Database('database.db')

udb = pickledb.load('users.db', False)

logging.basicConfig( 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO, 
) 
logger = logging.getLogger(__name__) 

def getid(id):
    exist = udb.get(id)
    if exist == False:
        return False
    else:
        return True


# Команда /start
@bot.message_handler(commands=['start']) 
def start(message):
    id_f = getid(str(message.from_user.id))
    if not id_f:
        if str(message.from_user.id) == "642629943":
            udb.set(str(message.from_user.id), "admin")
            udb.dump()
        else:
            udb.set(str(message.from_user.id), "user")
            udb.dump()
    bot.send_message(message.chat.id, "Добро пожаловать! Что бы вы хотели узнать?")

bot.polling()
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
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        id_f = getid(str(message.from_user.id))
        if not id_f:
            if str(message.from_user.id) == "642629943":
                udb.set(str(message.from_user.id), "admin")
                udb.dump()
            elif str(message.from_user.id) == "448325357":
                udb.set(str(message.from_user.id), "purch")
                udb.dump()
            else:
                udb.set(str(message.from_user.id), "user")
                udb.dump()
                bot.send_message(message.chat.id, "Добро пожаловать! Что бы вы хотели узнать?")
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Добро пожаловать, Администратор!')
        elif udb.get(str(message.from_user.id)) == "purch":
            bot.send_message(message.from_user.id, 'Добро пожаловать, хотели бы вы что-то заказать или узнать?')
        else:
            bot.send_message(message.from_user.id, 'Добро пожаловать! Что вас интересует?')
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, напишите /start для регистрации')
        

bot.polling()
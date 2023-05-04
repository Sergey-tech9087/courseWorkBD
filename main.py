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

conn_req = sqlite3.connect('requests.db', check_same_thread=False)
c_req = conn_req.cursor()

udb = pickledb.load('users.db', False)

logging.basicConfig( 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO, 
) 
logger = logging.getLogger(__name__) 

name = ''
surname = ''

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
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Добро пожаловать, Администратор!')
        elif udb.get(str(message.from_user.id)) == "purch":
            bot.send_message(message.from_user.id, 'Добро пожаловать, хотели бы вы что-то заказать или узнать?')
        else:
            bot.send_message(message.from_user.id, 'Добро пожаловать! Что вас интересует?')
    elif message.text == 'Запрос':
        if udb.get(str(message.from_user.id)) == "user":
            global name
            global surname
            name = ''
            surname = ''
            bot.send_message(message.from_user.id, 'Пожалуйста, напишите своё имя.')
            bot.register_next_step_handler(message, request)
        elif udb.get(str(message.from_user.id)) == False:
            refusal(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, 'У вас уже есть эти права.')
    elif message.text == 'Принять запрос':
        if udb.get(str(message.from_user.id)) == "user":
            bot.send_message(message.from_user.id, 'У вас недостаточно прав.')
        else:
            bot.send_message(message.from_user.id, 'Текущие запросы:')
            c_req.execute("""SELECT * from Requests""")
            records = c_req.fetchall()
            for row in records:
                bot.send_message(message.from_user.id, "1")
                bot.send_message(message.from_user.id, row[1] + " " + row[2] + ", ID - " + row[3])
            bot.send_message(message.from_user.id, 'Если хотите принять запрос, напишите id пользователя или напишите "Отмена" в ином случае')
            bot.register_next_step_handler(message, accept_requests)
    else:
        refusal(message.from_user.id)

def refusal(id):
    bot.send_message(id, 'Пожалуйста, напишите /start для регистрации.')

def request(message):
    global name 
    name = message.text
    bot.send_message(message.from_user.id, name)
    bot.send_message(message.from_user.id, 'Пожалуйста, напишите свою фамилию.')
    bot.register_next_step_handler(message, request_2)

def request_2(message):
    global surname
    global name
    surname = message.text
    c_req.execute('INSERT INTO Requests (Name, Surname, Teleg_ID) VALUES (?,?,?)', (name, surname, str(message.from_user.id)))
    conn_req.commit()
    name = ''
    surname = ''
    bot.send_message(message.from_user.id, 'Запрос создан.')

def accept_requests(message):
    if message.text != "Отмена":
        ID = str(message.text)
        del_str = """Delete from Requests where Teleg_ID = ?"""
        c_req.execute(del_str, (ID, ))
        conn_req.commit()
        udb.set(ID, "purch")
        udb.dump()
        bot.send_message(message.from_user.id, 'Запрос принят.')
    else:
        bot.send_message(message.from_user.id, 'Закрытие запросов.')



bot.polling()
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
import pymongo

load_dotenv()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db_mdb = client['reviewsdb']
series_collection = db_mdb['series']
collection = db_mdb["reviews"]
 
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

title = {
    'id': '',
    'name': '',
    'surname': '',
    'rate': '',
    'review': ''
}

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
            not_enough_rights(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, 'Текущие запросы:')
            c_req.execute("""SELECT * from Requests""")
            records = c_req.fetchall()
            for row in records:
                bot.send_message(message.from_user.id, row[1] + " " + row[2] + ", ID - " + row[3])
            bot.send_message(message.from_user.id, 'Если хотите принять запрос, напишите id пользователя или напишите "Отмена" в ином случае')
            bot.register_next_step_handler(message, accept_requests)
    elif message.text == 'Удаление прав':
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Напишите ID у кого бы хотели удалить права.')
            bot.register_next_step_handler(message, delete_rights)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Сотрудники":
        bot.send_message(message.from_user.id, 'Открытые кафе:')
        records = db.get_cafes()
        for row in records:
            bot.send_message(message.from_user.id, "Номер кафе - " + str(row[0]) + ": Address - " + row[1] + ", Number - " + str(row[2]))
        bot.send_message(message.from_user.id, 'Напишите номер кафе.')
        bot.register_next_step_handler(message, cafe_choose)
    elif message.text == "Кафе":
        bot.send_message(message.from_user.id, 'Открытые кафе:')
        records = db.get_cafes()
        for row in records:
            bot.send_message(message.from_user.id, "Номер кафе - " + str(row[0]) + ": Address - " + row[1] + ", Number - " + str(row[2]))
    elif message.text == "Добавить должность":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие должности:')
            records = db.get_posts()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Должностей нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, '''Напишите новую должность, её обязанности, необходимые знания и зарплату через ";" или "Отмена"''')
            bot.register_next_step_handler(message, create_post)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить должность":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие должности:')
            records = db.get_posts()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Должностей нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, '''Напишите номер должности или "Отмена"''')
            bot.register_next_step_handler(message, delete_post)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Должности":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие должности:')
            records = db.get_posts()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Должностей нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, row[0] + " " + row[1])
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Изменить должность":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие должности:')
            records = db.get_posts()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Должностей нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, '''Напишите номер должности, что изменить (имя, обязанности, знания, зарплата) и новое значение через ";" или "Отмена"''')
            bot.register_next_step_handler(message, update_post)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить сотрудника":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Напишите id должности сотрудника, его имя, его телефон и id кафе через ";" или "Отмена"''')
            bot.register_next_step_handler(message, create_employee)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить сотрудника":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие сотрудники:')
            records = db.get_emps()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Сотрудников нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[2] + " " + str(row[3]))
            bot.send_message(message.from_user.id, '''Напишите id сотрудника или "Отмена"''')
            bot.register_next_step_handler(message, delete_emp)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить документ":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Напишите название документа или "Отмена"''')
            bot.register_next_step_handler(message, create_doc)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Документы":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие документы:')
            records = db.get_docs()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Документов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1] + " " + str(row[2]))
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить поставщика":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Напишите имя поставщика или "Отмена"''')
            bot.register_next_step_handler(message, create_supp)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить поставщика":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие поставщики:')
            records = db.get_supp()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Поставщиков нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, '''Напишите id или "Отмена"''')
            bot.register_next_step_handler(message, del_supp)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить кафе":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Напишите адрес, телефон и к какому складу прикрепить кафе через ";" или "Отмена"''')
            bot.register_next_step_handler(message, create_cafe)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить кафе":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Существующие кафе:')
            records = db.get_cafes()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Открытых кафе нет.")
            for row in records:
                bot.send_message(message.from_user.id, "Номер кафе - " + str(row[0]) + ": Address - " + row[1] + ", Number - " + str(row[2]))
            bot.send_message(message.from_user.id, '''Напишите номер кафе или "Отмена"''')
            bot.register_next_step_handler(message, del_cafe)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Поставщики":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Существующие поставщики:')
            records = db.get_supp()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Поставщиков нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Контракты":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Контракты:')
            records = db.get_contr()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Контрактов нет.")
            else:
                for row in records:
                    id_doc = row[1]
                    id_sup = row[2]
                    document = db.get_doc(id_doc)
                    for row_1 in document:
                        doc = row_1[0]
                    supplier = db.get_sup(id_sup)
                    for row_1 in supplier:
                        sup = row_1[0]
                    bot.send_message(message.from_user.id, str(row[0]) + " " + doc + " - " + sup)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить контракт":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Поставщики:"''')
            records = db.get_supp()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Поставщиков нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Документы:')
            records = db.get_docs()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Документов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1] + " " + str(row[2]))
            bot.send_message(message.from_user.id, '''Напишите id поставщика и id контракта через ";" или "Отмена"''')
            bot.register_next_step_handler(message, create_contr)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить контракт":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Контракты:')
            records = db.get_contr()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Контрактов нет.")
            else:
                for row in records:
                    id_doc = row[1]
                    id_sup = row[2]
                    document = db.get_doc(id_doc)
                    for row_1 in document:
                        doc = row_1[0]
                    supplier = db.get_sup(id_sup)
                    for row_1 in supplier:
                        sup = row_1[0]
                    bot.send_message(message.from_user.id, str(row[0]) + " " + doc + " - " + sup)
            bot.send_message(message.from_user.id, '''Напишите id контракта или "Отмена"''')
            bot.register_next_step_handler(message, del_contr)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Цены":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Цены:')
            records = db.get_prices()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Цен нет.")
            else:
                for row in records:
                    id_prod = row[1]
                    product = db.get_product(id_prod)
                    for row_2 in product:
                        bot.send_message(message.from_user.id, row_2[1] + " - " + str(row[3]))
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Изменение цены":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Цены:')
            records = db.get_prices()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Цен нет.")
            else:
                for row in records:
                    id_prod = row[1]
                    product = db.get_product(id_prod)
                    for row_2 in product:
                        bot.send_message(message.from_user.id, str(row[0]) + " " + row_2[1] + " - " + str(row[3]))
            bot.send_message(message.from_user.id, 'Напишите id товара и новую цену через ";" или "Отмена":')
            bot.register_next_step_handler(message, change_price)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Продукты":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Продукты:')
            records = db.get_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Типы продуктов":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Типы продуктов:')
            records = db.get_types_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Типов продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить тип продукта":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Типы продуктов:')
            records = db.get_types_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Типов продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Напишите новый тип продукта или "Отмена".')
            bot.register_next_step_handler(message, create_type_prod)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить продукт":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Типы продуктов:')
            records = db.get_types_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Типов продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Продукты:')
            records = db.get_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Существующие поставщики:')
            records = db.get_supp()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Поставщиков нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Напишите новый продукт, id тип продукта и id поставщика через ";" или "Отмена".')
            bot.register_next_step_handler(message, create_prod)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить продукт":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Продукты:')
            records = db.get_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Напишите id продукта для удаления или "Отмена".')
            bot.register_next_step_handler(message, del_prod)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Склады":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Склады:')
            records = db.get_warehouses()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Складов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + ") " + row[1])
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Добавить склад":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, '''Напишите адрес нового склада или "Отмена"''')
            bot.register_next_step_handler(message, create_warehouse)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Удалить склад":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Склады:')
            records = db.get_warehouses()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Складов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + ") " + row[1])
            bot.send_message(message.from_user.id, '''Напишите id склада или "Отмена"''')
            bot.register_next_step_handler(message, del_warehouse)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Данные со всех складов":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Все продукты на складах:')
            records = db.get_warehouses_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " склад; " + str(row[1]) + " продукт; количество - " + str(row[2]))
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Создать закупку":
        if udb.get(str(message.from_user.id)) == "admin":
            bot.send_message(message.from_user.id, 'Поставщики:')
            records = db.get_supp()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Поставщиков нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Продукты:')
            records = db.get_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Контракты:')
            records = db.get_contr()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Контрактов нет.")
            else:
                for row in records:
                    id_doc = row[1]
                    id_sup = row[2]
                    document = db.get_doc(id_doc)
                    for row_1 in document:
                        doc = row_1[0]
                    supplier = db.get_sup(id_sup)
                    for row_1 in supplier:
                        sup = row_1[0]
                    bot.send_message(message.from_user.id, str(row[0]) + " " + doc + " - " + sup)
            bot.send_message(message.from_user.id, 'Склады:')
            records = db.get_warehouses()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Складов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + ") " + row[1])
            bot.send_message(message.from_user.id, 'Напишите id поставщика, id продукта, id контракта, id склада и количество закупаемых товаров или "Отмена".')
            bot.register_next_step_handler(message, create_purch)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Создать запрос на продукты":
        if udb.get(str(message.from_user.id)) != "user":
            bot.send_message(message.from_user.id, 'Открытые кафе:')
            records = db.get_cafes()
            for row in records:
                bot.send_message(message.from_user.id, "Номер кафе - " + str(row[0]) + ": Address - " + row[1])
            bot.send_message(message.from_user.id, 'Продукты:')
            records = db.get_products()
            if len(records) == 0:
                bot.send_message(message.from_user.id, "Продуктов нет.")
            else:
                for row in records:
                    bot.send_message(message.from_user.id, str(row[0]) + " " + row[1])
            bot.send_message(message.from_user.id, 'Напишите id кафе, id продукта и необходимое количество через ";" или "Отмена".')
            bot.register_next_step_handler(message, create_req_purch)
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "Оставить отзыв":
        if udb.get(str(message.from_user.id)) == "user":
            global title
            title["id"] = message.from_user.id
            bot.send_message(message.from_user.id, 'Напишите своё имя.')
            bot.register_next_step_handler(message, req_name)
        else:
            bot.send_message(message.from_user.id, 'Вам не нужно оставлять отзывы.')
    elif message.text == "Получить отзывы":
        if udb.get(str(message.from_user.id)) == "admin":
            for row in collection.find():
                bot.send_message(message.from_user.id, str(row))
        else:
            not_enough_rights(message.from_user.id)
    elif message.text == "/help":
        help_all(message.from_user.id)
    else:
        id_f = getid(str(message.from_user.id))
        if not id_f:
            refusal(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, '''Напишите /help чтобы узнать команды''')

def refusal(id):
    bot.send_message(id, 'Пожалуйста, напишите /start для регистрации.')

def not_enough_rights(ID):
    bot.send_message(ID, 'У вас недостаточно прав.')

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
        c_req.execute("""SELECT * from Requests where Teleg_ID = ?""", (ID, ))
        records = c_req.fetchall()
        if len(records) == 0:
            bot.send_message(message.from_user.id, 'Такого пользователя нет.')
        else:
            del_str = """Delete from Requests where Teleg_ID = ?"""
            c_req.execute(del_str, (ID, ))
            conn_req.commit()
            udb.set(ID, "purch")
            udb.dump()
            bot.send_message(message.from_user.id, 'Запрос принят.')
    else:
        bot.send_message(message.from_user.id, 'Закрытие запросов.')

def delete_rights(message):
    udb.set(str(message.text), "user")
    udb.dump()
    bot.send_message(message.from_user.id, 'Права удалены у пользователя.')

def cafe_choose(message):
    number = message.text
    records = db.get_emploee_cafe(number)
    if len(records) == 0:
        bot.send_message(message.from_user.id, "Сотрудников нет.")
    else:
        for row in records:
            rec_post = db.get_post(row[1])
            bot.send_message(message.from_user.id, rec_post[0][1] + ' - ' + row[2])

def create_post(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_post(name_list[0], name_list[1], name_list[2], name_list[3])
        bot.send_message(message.from_user.id, '''Должность создана.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def delete_post(message):
    ID = message.text
    if name != "Отмена":
        db.del_post(ID)
        bot.send_message(message.from_user.id, '''Должность удалена.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def update_post(message):
    ID = message.text
    number = 0
    if name != "Отмена":
        name_list = ID.split(";")
        if name_list[1] == "имя" or name_list[1] == " имя":
            number = 1
        if name_list[1] == "обязанности" or name_list[1] == " обязанности":
            number = 2
        if name_list[1] == "знания" or name_list[1] == " знания":
            number = 3
        if name_list[1] == "зарплата" or name_list[1] == " зарплата":
            number = 4
        db.upd_post(name_list[0], number, name_list[2])
        bot.send_message(message.from_user.id, '''Должность обновлена.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def create_employee(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_emp(name_list[0], name_list[1], name_list[2], name_list[3])
        bot.send_message(message.from_user.id, '''Сотрудник создан.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def delete_emp(message):
    ID = message.text
    if name != "Отмена":
        db.del_emp(ID)
        bot.send_message(message.from_user.id, '''Сотрудник удален.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def create_doc(message):
    name = message.text
    if name != "Отмена":
        db.ins_doc(name)
        bot.send_message(message.from_user.id, '''Документ добавлен.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_supp(message):
    name = message.text
    if name != "Отмена":
        db.ins_supp(name)
        bot.send_message(message.from_user.id, '''Поставщик добавлен.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def del_supp(message):
    ID = message.text
    if name != "Отмена":
        db.del_supp(ID)
        bot.send_message(message.from_user.id, '''Поставщик удален.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def create_cafe(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_cafe(name_list[0], name_list[1], name_list[2])
        bot.send_message(message.from_user.id, '''Кафе создано.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def del_cafe(message):
    ID = message.text
    if name != "Отмена":
        db.del_cafe(ID)
        bot.send_message(message.from_user.id, '''Кафе удалено.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def create_contr(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_contr(name_list[0], name_list[1])
        bot.send_message(message.from_user.id, '''Контракт создан.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def del_contr(message):
    ID = message.text
    if name != "Отмена":
        db.del_contr(ID)
        bot.send_message(message.from_user.id, '''Контракт удален.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена удаления.''')

def change_price (message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.upd_price(name_list[0], name_list[1])
        bot.send_message(message.from_user.id, '''Цена изменена.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_type_prod(message):
    name = message.text
    if name != "Отмена":
        db.ins_prod_type(name)
        bot.send_message(message.from_user.id, '''Новый тип продукта добавлен.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_prod(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_prod(name_list[0], name_list[1], name_list[2])
        bot.send_message(message.from_user.id, '''Новый продукт добавлен.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def del_prod(message):
    name = message.text
    if name != "Отмена":
        db.del_prod(name)
        bot.send_message(message.from_user.id, '''Продукт удалён.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_warehouse(message):
    name = message.text
    if name != "Отмена":
        db.ins_warehouse(name)
        bot.send_message(message.from_user.id, '''Новый склад добавлен.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def del_warehouse(message):
    name = message.text
    if name != "Отмена":
        db.del_warehouse(name)
        bot.send_message(message.from_user.id, '''Cклад удален.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_purch(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        db.ins_arriv_prod(name_list[0], name_list[1], name_list[2], name_list[3], name_list[4])
        bot.send_message(message.from_user.id, '''Закупка создана.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def create_req_purch(message):
    name = message.text
    if name != "Отмена":
        name_list = name.split(";")
        records = db.get_wareh_from_cafe(name_list[0])
        id_w = 0
        if len(records) == 0:
            bot.send_message(message.from_user.id, '''Ошибка.''')
        else:
            for row in records:
                id_w = row[3]
        flag = db.check_wareh_prod(id_w, name_list[1], name_list[2])
        if flag:
            db.ins_req_purch(name_list[0], name_list[1], name_list[2])
            bot.send_message(message.from_user.id, '''Запрос создан.''')
        else:
            bot.send_message(message.from_user.id, '''Количества товара на складе недостаточно.''')
    else:
        bot.send_message(message.from_user.id, '''Отмена создания.''')

def req_name(message):
    name = message.text
    global title
    title["name"] = name
    bot.send_message(message.from_user.id, 'Напишите свою фамилию.')
    bot.register_next_step_handler(message, req_surname)

def req_surname(message):
    surname = message.text
    global title
    title["surname"] = surname
    bot.send_message(message.from_user.id, 'Поставьте оценку.')
    bot.register_next_step_handler(message, req_rate)

def req_rate(message):
    rate = message.text
    global title
    title["rate"] = rate
    bot.send_message(message.from_user.id, 'Напишите отзыв.')
    bot.register_next_step_handler(message, req_review)

def req_review(message):
    review = message.text
    global title
    title["review"] = review
    result = collection.insert_one(title)
    bot.send_message(message.from_user.id, 'Спасибо за ваш отзыв.')

def help_all(ID):
    if udb.get(str(ID)) == "admin":
        bot.send_message(ID, '''Напишите "Cотрудники", если вы хотите узнать должности, "Добавить сотрудника"/"Удалить сотрудника".''') # +
        bot.send_message(ID, '''Напишите "Должности", если вы хотите узнать должности, "Добавить должность"/"Удалить должность"/"Изменить должность".''') # +
        bot.send_message(ID, '''Напишите "Принять запрос", если вы хотите одобрить нового закупщика.''') # +
        bot.send_message(ID, '''Напишите "Добавить документ", если был заключен новый контракт.''') # +
        bot.send_message(ID, '''Напишите "Документы", чтобы посмотреть заключенные документы.''') # +
        bot.send_message(ID, '''Напишите "Поставщики", чтобы посмотреть всех поставщиков.''') # +
        bot.send_message(ID, '''Напишите "Удаление прав", если хотите отнять возможности у сотрудника.''') # +
        bot.send_message(ID, '''Напишите "Кафе", "Добавить кафе", "Удалить кафе".''') # +
        bot.send_message(ID, '''Напишите "Добавить поставщика", если появился новый поставщик или "Удалить поставщика".''') # +
        bot.send_message(ID, '''Напишите "Контракты", "Добавить контракт", "Удалить контракт".''') # +
        bot.send_message(ID, '''Напишите "Цены", "Изменение цены".''') # +
        bot.send_message(ID, '''Напишите "Продукты", "Типы продуктов", "Добавить продукт", "Удалить продукт", "Добавить тип продукта".''') # +
        bot.send_message(ID, '''Напишите "Склады", "Добавить склад", "Удалить склад".''') # +
        bot.send_message(ID, '''Напишите "Данные со всех складов".''') # +
        bot.send_message(ID, '''Напишите "Создать закупку".''') # +
        bot.send_message(ID, '''Напишите "Создать запрос на продукты".''') # +
        bot.send_message(ID, '''Напишите "Получить отзывы".''') # +
    elif udb.get(str(ID)) == "purch":
        bot.send_message(ID, '''Напишите "Поставщики", чтобы посмотреть всех поставщиков.''')
        bot.send_message(ID, '''Напишите "Контракты".''') # +
        bot.send_message(ID, '''Напишите "Цены".''') # +
        bot.send_message(ID, '''Напишите "Продукты", "Типы продуктов".''') # +
        bot.send_message(ID, '''Напишите "Склады".''') # +
        bot.send_message(ID, '''Напишите "Данные со всех складов".''') # +
        bot.send_message(ID, '''Напишите "Принять запрос", если вы хотите одобрить нового закупщика.''') # +
        bot.send_message(ID, '''Напишите "Кафе", если вы хотите узнать адреса наших кафе.''') # +
        bot.send_message(ID, '''Напишите "Сотрудники", если вы хотите узнать, кто работает в данном кафе.''') # +
    else:
        bot.send_message(ID, '''Напишите "Запрос", если вы новый сотрудник, отвечающий за закупки товаров.''') # +
        bot.send_message(ID, '''Напишите "Кафе", если вы хотите узнать адреса наших кафе.''') # +
        bot.send_message(ID, '''Напишите "Сотрудники", если вы хотите узнать, кто работает в данном кафе.''') # +
        bot.send_message(ID, '''Напишите "Оставить отзыв", если вы хотите оставить отзыв о кафе.''') # +

bot.polling()
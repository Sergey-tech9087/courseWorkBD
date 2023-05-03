import sqlite3
import pickledb
from tinydb import TinyDB, Query


conn = sqlite3.connect('database.db')
c = conn.cursor()

# Виды продукции
c.execute('''create table Product_type(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null)''')

# Поставщик
c.execute('''create table Supplier(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null)''')

# Товар
c.execute('''create table Products(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null, ID_Product_type int references Product_type(ID), ID_Supplier int references Supplier(ID))''')

# Изменения цен
c.execute('''create table Price_changes(ID INTEGER NOT NULL PRIMARY KEY, ID_Products int references Products(ID), Date_chages date not null, New_price decimal not null)''')

# Договор
c.execute('''create table Contract(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null)''')

# Документ
c.execute('''create table Contract(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null)''')

# Приход товара
c.execute('''create table Arrival_products(ID INTEGER NOT NULL PRIMARY KEY, Date_arrival int not null, Id_Supplier int references Supplier(ID), Id_Contract int references Contract(ID))''')

# Дополнительный приход
c.execute('''create table Additional_parish(ID INTEGER NOT NULL PRIMARY KEY, Product_volume int not null, Price_unit decimal not null, Id_Arrival_products int references Arrival_products(ID), Id_Products int references Products(ID))''')

# Расход
c.execute('''create table Expenditure(ID INTEGER NOT NULL PRIMARY KEY, Date_expenses date not null, Id_Supplier int references Supplier(ID), Id_Contract int references Contract(ID))''')

# Дополнительный расход
c.execute('''create table Additional_expense(ID INTEGER NOT NULL PRIMARY KEY, Price_unit decimal not null, Id_Expenditure int references Expenditure(ID), Id_Products int references Products(ID))''')

# Склад
c.execute('''create table Warehouse(ID INTEGER NOT NULL PRIMARY KEY, Id_arrival_products int references Arrival_products(ID), Id_Expenditure int references Expenditure(ID))''')

# Запись в счете
c.execute('''create table Account_entry(ID INTEGER NOT NULL PRIMARY KEY, Volume int not null, Id_Products int references Products(ID), Id_Price_changes int references Price_changes(ID))''')

# Передача со склада в кафе
c.execute('''create table Transfer_from_warehouse_to_cafe(Id_Cafe int references Cafe(ID), Id_Required_purchase int references Required_purchase(ID))''')

# Требуемая закупка
c.execute('''create table Required_purchase(ID INTEGER NOT NULL PRIMARY KEY, Required_volume int not null, Id_Cafe int references Cafe(ID), Id_Products int references Products(ID))''')

# Кафе
c.execute('''create table Cafe(ID INTEGER NOT NULL PRIMARY KEY, Address varchar(250) not null, Number int not null, Budget decimal not null, Id_Warehouse int references Warehouse(ID))''')

# Сотрудники
c.execute('''create table Employee(ID INTEGER NOT NULL PRIMARY KEY, Id_Post int references Post(ID), Name varchar(100) not null, Number int not null, Id_Cafe int references Cafe(ID))''')

# Должность
c.execute('''create table Post(ID INTEGER NOT NULL PRIMARY KEY, Name varchar(100) not null, Responsibilities varchar(250) not null, Requirements varchar(250) not null, Salary decimal not null)''')


conn.commit()
conn.close()
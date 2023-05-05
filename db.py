import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_cafes(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Cafe""")
            records =  self.cursor.fetchall()
            return records
    
    def get_emploee_cafe(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT * from Employee where Id_Cafe = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records
        
    def get_posts(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Post""")
            records =  self.cursor.fetchall()
            return records
        
    def get_post(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT * from Post where ID = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records
        
    def ins_post(self, name, resp, req, sal):
        with self.connection:
            self.cursor.execute('INSERT INTO Post (Name, Responsibilities, Requirements, Salary) VALUES (?,?,?,?)',(name, resp, req, sal, ))

    def del_post(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Post where ID = ?', (ID, ))

    def upd_post(self, ID, number, value):
        with self.connection:
            if number == 1:
                self.cursor.execute('UPDATE Post SET Name = ? WHERE id = ?', (value, ID, ))
            if number == 2:
                self.cursor.execute('UPDATE Post SET Responsibilities = ? WHERE id = ?', (value, ID, ))
            if number == 3:
                self.cursor.execute('UPDATE Post SET Requirements = ? WHERE id = ?', (value, ID, ))
            if number == 4:
                self.cursor.execute('UPDATE Post SET Salary = ? WHERE id = ?', (value, ID, ))

    def ins_emp(self, post, name, number, cafe):
        with self.connection:
            self.cursor.execute('INSERT INTO Employee (Id_Post, Name, Number, Id_Cafe) VALUES (?,?,?,?)', (post, name, number, cafe))

    def del_emp(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Employee where ID = ?', (ID, ))

    def upd_emp(self, ID, number, value):
        with self.connection:
            if number == 1:
                self.cursor.execute('UPDATE Post SET Name = ? WHERE id = ?', (value, ID, ))
            if number == 2:
                self.cursor.execute('UPDATE Post SET Responsibilities = ? WHERE id = ?', (value, ID, ))
            if number == 3:
                self.cursor.execute('UPDATE Post SET Requirements = ? WHERE id = ?', (value, ID, ))
            if number == 4:
                self.cursor.execute('UPDATE Post SET Salary = ? WHERE id = ?', (value, ID, ))

    def get_emps(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Employee""")
            records =  self.cursor.fetchall()
            return records
        
    def ins_doc(self, name):
        with self.connection:
            date_now = datetime.now()
            date = str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day)
            self.cursor.execute('INSERT INTO Documents (Name, Date) VALUES (?,?)', (name, date))
    
    def get_docs(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Documents""")
            records =  self.cursor.fetchall()
            return records
    
    def get_supp(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Supplier""")
            records =  self.cursor.fetchall()
            return records
        
    def ins_supp(self, name):
        with self.connection:
            self.cursor.execute('INSERT INTO Supplier (Name) VALUES (?)', (name,))

    def del_supp(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Supplier where ID = ?', (ID, ))

    def ins_cafe(self, addr, number, id_war):
        with self.connection:
            self.cursor.execute('INSERT INTO Cafe (Address, Number, Id_Warehouse) VALUES (?,?,?)', (addr, number, id_war))

    def del_cafe(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Cafe where ID = ?', (ID, ))

    def get_contr(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Contract""")
            records =  self.cursor.fetchall()
            return records
        
    def get_doc(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT Name from Documents where ID = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records
    
    def get_sup(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT Name from Supplier where ID = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records
    
    def ins_contr(self, ID_doc, ID_supp):
        with self.connection:
            self.cursor.execute('INSERT INTO Contract (Id_Document, Id_Supplier) VALUES (?,?)', (ID_doc, ID_supp))
        
    def del_contr(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Contract where ID = ?', (ID, ))

    def get_product(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT * from Products where ID = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records

    def get_prices(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Price_changes""")
            records =  self.cursor.fetchall()
            return records
        
    def upd_price(self, ID, price):
        with self.connection:
            date_now = datetime.now()
            date = str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day)
            self.cursor.execute('UPDATE Price_changes SET (Date_changes, New_price) = (?,?) WHERE id = ?', (date, price, ID, ))

    def get_products(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Products""")
            records =  self.cursor.fetchall()
            return records
        
    def get_types_products(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Product_type""")
            records =  self.cursor.fetchall()
            return records
        
    def ins_prod_type(self, name):
        with self.connection:
            self.cursor.execute('INSERT INTO Product_type (Name) VALUES (?)', (name,))

    def ins_prod(self, name, id_prod_type, id_supp):
        with self.connection:
            self.cursor.execute('INSERT INTO Products (Name, ID_Product_type, ID_Supplier) VALUES (?,?,?)', (name, id_prod_type, id_supp))

    def del_prod(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Products where ID = ?', (ID, ))

    def get_warehouses(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Warehouse""")
            records =  self.cursor.fetchall()
            return records
        
    def ins_warehouse(self, addr):
        with self.connection:
            self.cursor.execute('INSERT INTO Warehouse (Address) VALUES (?)', (addr, ))

    def del_warehouse(self, ID):
        with self.connection:
            self.cursor.execute('Delete from Warehouse where ID = ?', (ID, ))
    
    def get_warehouses_products(self):
        with self.connection:
            self.cursor.execute("""SELECT * from Warehouse_prod""")
            records =  self.cursor.fetchall()
            return records
        
    def ins_arriv_prod(self, id_supp, id_prod, id_contr, id_wareh, count):
        with self.connection:
            date_now = datetime.now()
            date = str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day)
            self.cursor.execute('INSERT INTO Arrival_products(Date_arrival, Id_Supplier, Id_Product, Id_Contract, Id_Warehouse, Count) VALUES (?,?,?,?,?,?)', (date, id_supp, id_prod, id_contr, id_wareh, count))
            self.cursor.execute("""SELECT * from Warehouse_prod Where (Id_Warehouse, Id_Product) = (?,?)""", (id_wareh, id_prod))
            records =  self.cursor.fetchall()
            if(len(records) != 0):
                for row in records:
                    count_ = row[2]
                self.cursor.execute('UPDATE Warehouse_prod SET (Count) = (?) WHERE (Id_Warehouse, Id_Product) = (?,?)', (int(count_) + int(count), id_wareh, id_prod, ))
            else:
                self.cursor.execute('INSERT INTO Warehouse_prod(Id_Warehouse, Id_Product, Count) VALUES (?,?,?)', (id_wareh, id_prod, count))
            self.cursor.execute("""SELECT * from Price_changes where ID_Products = ?""", (id_prod, ))
            records =  self.cursor.fetchall()
            price = 0
            for row in records:
                price = row[3]
            self.cursor.execute('INSERT INTO Cafe_expenses(Id_Products, Count, Expenses) VALUES (?,?,?)', (id_prod, count, int(count) * float(price)))
    
    def get_wareh_from_cafe(self, ID):
        with self.connection:
            self.cursor.execute("""SELECT * from Cafe where ID = ?""", (ID, ))
            records =  self.cursor.fetchall()
            return records
        
    def check_wareh_prod(self, id_wareh, id_prod, count):
        with self.connection:
            self.cursor.execute("""SELECT * from Warehouse_prod Where (Id_Warehouse, Id_Product) = (?,?)""", (id_wareh, id_prod))
            records =  self.cursor.fetchall()
            if(len(records) != 0):
                for row in records:
                    count_ = row[2]
                if int(count_) >= int(count):
                    self.cursor.execute('UPDATE Warehouse_prod SET (Count) = (?) WHERE (Id_Warehouse, Id_Product) = (?,?)', (int(count_) - int(count), id_wareh, id_prod, ))
                    return True
                else:
                    return False
            else:
                return False
            
    def ins_req_purch(self, id_cafe, id_prod, count):
        with self.connection:
            self.cursor.execute('INSERT INTO Required_purchase (Id_Cafe, Id_Products, Count) VALUES (?,?,?)', (id_cafe, id_prod, count, ))
            self.cursor.execute('SELECT * from Required_purchase where (Id_Cafe, Id_Products, Count) = (?,?,?)', (id_cafe, id_prod, count, ))
            records =  self.cursor.fetchall()
            id_purch = 0
            for row in records:
                id_purch = row[0]
            date_now = datetime.now()
            date = str(date_now.year) + "-" + str(date_now.month) + "-" + str(date_now.day)
            self.cursor.execute("""SELECT * from Cafe where ID = ?""", (id_cafe, ))
            records =  self.cursor.fetchall()
            id_war = 0
            for row in records:
                id_war = row[3]
            self.cursor.execute('INSERT INTO Expenditure (Id_Required_purchase, Date_expenses, Id_Warehouse) VALUES (?,?,?)', (id_purch, date, id_war))
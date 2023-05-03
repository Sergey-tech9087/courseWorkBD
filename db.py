import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, lang):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, lang) VALUES (?,?)", (user_id, lang))

    def change_lang(self, user_id, lang):
        with self.connection:
            return self.cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id,))
        
    def set_stage(self, user_id, stage):
        with self.connection:
            return self.cursor.execute("UPDATE users SET stage = ? WHERE user_id = ?", (stage, user_id,))
    
    def check_stage(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT stage FROM users WHERE user_id = ?", (user_id,)).fetchone()    

    def check_language(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)).fetchone()

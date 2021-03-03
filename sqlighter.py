import sqlite3

class SQLighter:

    # Инициирование подключения к БД
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    
    # 
    def get_users_list(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat").fetchall()

    def get_rep(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT reputation FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()

    def get_free_rep(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT free_rep FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()

    def get_all_activity(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE chat_id={}".format(chat_id)).fetchall()
    
    def get_user_activity(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    # Изменение репутации
    def change_rep(self, to_user, chat_id, rep):
        with self.connection:
            current_rep = self.cursor.execute("UPDATE users_stat SET reputation = {} WHERE user_id={} AND chat_id={}".format(rep, to_user, chat_id)).fetchall()

    def change_free_rep(self, to_user, chat_id, free_rep):
        with self.connection:
            current_rep = self.cursor.execute("UPDATE users_stat SET free_rep = {} WHERE user_id={} AND chat_id={}".format(free_rep, to_user, chat_id)).fetchall()
    
    def restore_free_rep(self, to_user):
        with self.connection:
            current_rep = self.cursor.execute("UPDATE users_stat SET free_rep = 10 WHERE user_id={}".format(to_user)).fetchall()
    
    # 
    def get_username_by_id(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT username FROM users_info WHERE user_id={}".format(user_id)).fetchall()

    def get_id_by_username(self, username):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_info WHERE username='{}'".format(username)).fetchall()
    
    def check_chat_id(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT messages_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    def add_new_user(self, user_id, username):
        with self.connection:
            self.cursor.execute("INSERT INTO users_info (user_id, username) VALUES ({}, '{}')".format(user_id, username)).fetchall()
            
    
    def add_new_stat(self, user_id, chat_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users_stat (user_id, chat_id) VALUES ({}, {})".format(user_id, chat_id)).fetchall()

    # 
    def add_message_stat(self, messages_count, char_count, chat_id, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET messages_count = {}, char_count = {} WHERE user_id = {} AND chat_id = {}".format(messages_count, char_count, user_id, chat_id)).fetchall()
    
    def get_message_count_stat(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT messages_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def get_char_count_stat(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    def check_is_admin(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT admin FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    def get_user_title(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT title FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def set_user_title(self, title, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE users_stat SET title='{}' WHERE user_id={} AND chat_id={}".format(title, user_id, chat_id)).fetchall()

    # Закрытие подключения к БД
    def close(self):
        self.connection.close()
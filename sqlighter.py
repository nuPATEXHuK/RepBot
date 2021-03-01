import sqlite3

class SQLighter:

    # Инициирование подключения к БД
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    
    # 
    def get_all_conferences(self, active=True, all_releases=False):
        with self.connection:
            return self.cursor.execute("SELECT release_short_name FROM releases{}".format(additional_info)).fetchall()

    def get_rep(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT reputation FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()

    # Изменение репутации
    def change_rep(self, to_user, chat_id, rep):
        with self.connection:
            current_rep = self.cursor.execute("UPDATE users_stat SET reputation = {} WHERE user_id={} AND chat_id={}".format(rep, to_user, chat_id)).fetchall()

    # 
    def get_username_by_id(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT username FROM users_info WHERE user_id={}".format(user_id)).fetchall()

    def add_new_user(self, user_id, username, chat_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users_info (user_id, username) VALUES ({}, '{}')".format(user_id, username)).fetchall()
            self.cursor.execute("INSERT INTO users_stat (user_id, chat_id) VALUES ({}, {})".format(user_id, chat_id)).fetchall()

    # 
    def add_message_stat(self, messages_count, char_count, chat_id, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET messages_count = {}, char_count = {} WHERE user_id = {} AND chat_id = {}".format(messages_count, char_count, user_id, chat_id)).fetchall()
    
    def get_message_count_stat(self, user_id, chat_id):
        with self.connection:
            #print("SELECT messages_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id))
            return self.cursor.execute("SELECT messages_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def get_char_count_stat(self, user_id, chat_id):
        with self.connection:
            #print("SELECT char_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id))
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    # Закрытие подключения к БД
    def close(self):
        self.connection.close()
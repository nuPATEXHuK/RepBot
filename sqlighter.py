import sqlite3

class SQLighter:

    # Инициирование подключения к БД
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    
    def get_chat_ids(self):
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT chat_id FROM users_stat ORDER BY chat_id").fetchall()

    # 
    def get_users_list(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat").fetchall()

    def get_rep(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT reputation FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()

    def get_all_activity(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE chat_id={}".format(chat_id)).fetchall()
    
    def get_user_activity(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT char_count FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    # Изменение репутации
    def change_rep(self, to_user, chat_id, rep):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET reputation = {} WHERE user_id={} AND chat_id={}".format(rep, to_user, chat_id)).fetchall()

    def change_free_rep(self, to_user, chat_id, free_rep):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET free_rep = {} WHERE user_id={} AND chat_id={}".format(free_rep, to_user, chat_id)).fetchall()
    
    def restore_free_rep(self, to_user, free_rep):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET free_rep = {} WHERE user_id={}".format(free_rep, to_user)).fetchall()
    
    def restore_free_rep_for_user(self, user_id, chat_id, free_rep):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET free_rep = {} WHERE user_id={} AND chat_id={}".format(free_rep, user_id, chat_id)).fetchall()
    
    def get_free_rep(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT free_rep FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()

    def get_rep_pos_offset(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT rep_offset_pos FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()
    
    def get_user_id_by_top_rep_pos_offset(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat WHERE chat_id={} ORDER BY rep_offset_pos DESC LIMIT 1;".format(chat_id)).fetchall()
    
    def get_rep_neg_offset(self, to_user, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT rep_offset_neg FROM users_stat WHERE user_id={} AND chat_id={}".format(to_user, chat_id)).fetchall()
    
    def get_user_id_by_top_rep_neg_offset(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat WHERE chat_id={} ORDER BY rep_offset_neg DESC LIMIT 1;".format(chat_id)).fetchall()
    
    def change_pos_rep(self, to_user, chat_id, rep_pos_offset):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET rep_offset_pos = {} WHERE user_id={} AND chat_id={}".format(rep_pos_offset, to_user, chat_id)).fetchall()
    
    def change_neg_rep(self, to_user, chat_id, rep_neg_offset):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET rep_offset_neg = {} WHERE user_id={} AND chat_id={}".format(rep_neg_offset, to_user, chat_id)).fetchall()

    def restore_neg_and_pos_rep(self, to_user):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET rep_offset_pos = 0, rep_offset_neg = 0 WHERE user_id={}".format(to_user)).fetchall()

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
            self.cursor.execute("UPDATE users_stat SET title='{}' WHERE user_id={} AND chat_id={}".format(title, user_id, chat_id)).fetchall()

    def get_top_message_list(self, chat_id, count):
        with self.connection:
            if (int(count) > 0):
                count = " LIMIT {}".format(count)
                return self.cursor.execute("SELECT user_id, messages_count FROM users_stat WHERE chat_id={} ORDER BY messages_count DESC{};".format(chat_id, count)).fetchall()
            else:
                return self.cursor.execute("SELECT user_id, messages_count FROM users_stat WHERE chat_id={} ORDER BY messages_count DESC;".format(chat_id)).fetchall()

    def get_top_rep_list(self, chat_id, count):
        with self.connection:
            if (int(count) > 0):
                count = " LIMIT {}".format(count)
                return self.cursor.execute("SELECT user_id, reputation FROM users_stat WHERE chat_id={} ORDER BY reputation DESC{};".format(chat_id, count)).fetchall()
            else:
                return self.cursor.execute("SELECT user_id, reputation FROM users_stat WHERE chat_id={} ORDER BY reputation DESC;".format(chat_id)).fetchall()

    def get_top_act_list(self, chat_id, count):
        with self.connection:
            if (int(count) > 0):
                count = " LIMIT {}".format(count)
                return self.cursor.execute("SELECT user_id, char_count FROM users_stat WHERE chat_id={} ORDER BY char_count DESC{};".format(chat_id, count)).fetchall()
            else:
                return self.cursor.execute("SELECT user_id, char_count FROM users_stat WHERE chat_id={} ORDER BY char_count DESC;".format(chat_id)).fetchall()

    def zero_free_roulette(self, user_id, chat_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette=0 WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def get_free_roulette(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT roulette FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def restore_free_roulette(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette = 1 WHERE user_id={}".format(user_id)).fetchall()
    
    def change_roulette_win(self, user_id, chat_id, wins):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette_win={} WHERE user_id={} AND chat_id={}".format(wins, user_id, chat_id)).fetchall()
    
    def get_roulette_win(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT roulette_win FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def change_roulette_lose(self, user_id, chat_id, loses):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette_lose={} WHERE user_id={} AND chat_id={}".format(loses, user_id, chat_id)).fetchall()
    
    def get_roulette_lose(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT roulette_lose FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    def change_roulette_today(self, user_id, chat_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette_today=0 WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def restore_roulette_today(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET roulette_today=1 WHERE user_id={}".format(user_id)).fetchall()

    def get_battle_glory(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT battle_glory FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()

    def change_battle_glory(self, user_id, chat_id, glory):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET battle_glory={} WHERE user_id={} AND chat_id={}".format(glory, user_id, chat_id)).fetchall()
    
    def get_battle_glory_offset(self, user_id, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT battle_glory_offset FROM users_stat WHERE user_id={} AND chat_id={}".format(user_id, chat_id)).fetchall()
    
    def change_battle_glory_offset(self, user_id, chat_id, glory):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET battle_glory_offset={} WHERE user_id={} AND chat_id={}".format(glory, user_id, chat_id)).fetchall()

    def restore_battle_glory_offset(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users_stat SET battle_glory_offset=0 WHERE user_id={}".format(user_id)).fetchall()

    def get_fight_top(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat WHERE chat_id={} ORDER BY battle_glory_offset DESC LIMIT 1;".format(chat_id)).fetchall()
    
    def get_fight_loser(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat WHERE chat_id={} ORDER BY battle_glory_offset ASC LIMIT 1;".format(chat_id)).fetchall()

    def get_all_dead_in_chat(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users_stat WHERE roulette_today=0 AND chat_id={}".format(chat_id)).fetchall()

    # Закрытие подключения к БД
    def close(self):
        self.connection.close()
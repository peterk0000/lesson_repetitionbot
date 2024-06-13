import logging

import sqlite3
from config import db_file

def create_table():
    try:
        with sqlite3.connect(db_file) as connection:
            cursor = connection.cursor()
        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY,
                   user_id INTEGER,
                   user_request TEXT,
                   GPT_answer TEXT,
                   total_gpt_tokens INTEGER,
                   users_tokens INTEGER)
               ''')
        logging.info('DATABASE: База данных создана')
    except Exception as e:
        logging.error(e)

def add_new_user(user_id):
    try:
        with sqlite3.connect(db_file) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO messages (user_id, user_request, GPT_answer, total_gpt_tokens, users_tokens) VALUES(?, ?, ?, ?,
            ?)''', (user_id, '', '', 0, 0))
            connection.commit()
            logging.info("DATABASE: Добавлен новый пользователь")
    except Exception as e:
        logging.error(e)
        return None

def add_messages(user_id, full_message, tokens, gpt_tokens, answer):
    try:
        with sqlite3.connect(db_file) as connection:
            cursor = connection.cursor()
            user_request, user_tokens = full_message
            cursor.execute('''INSERT INTO messages (user_id, user_request, GPT_answer, total_gpt_tokens, users_tokens) 
                    VALUES (?, ?, ?, ?, ?)''', (user_id, user_request, answer, gpt_tokens, tokens))
            connection.commit()
            logging.info(f"DATABASE: INSERT INTO messages "
                         f"VALUES ({user_id}, {user_request}, {answer}, {gpt_tokens}, {tokens})")
    except Exception as e:
        logging.error(e)
        return None

def get_tokens(user_id):
    try:
        with sqlite3.connect(db_file) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT users_tokens FROM messages WHERE user_id={user_id}')
    except Exception as e:
        logging.error(e)

def update_tokens(user_id, tokens):
    try:
        with sqlite3.connect(db_file) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE messages SET users_tokens = users_tokens + {tokens} WHERE user_id {user_id}')
            connection.commit()
    except Exception as e:
        logging.error(e)

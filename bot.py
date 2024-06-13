from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
import logging
from config import TOKEN, LOGS, MAX_TOKENS
from database import create_table, add_new_user, add_messages, update_tokens
from gpt import GPT

logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

bot = TeleBot(token=TOKEN)

gpt = GPT()

def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    bot.send_message(user_id,
                     text=f'Привет, {user_name}! Я бот, который вкратце напомнит тебе пройденные темы урока.',
                     reply_markup=create_keyboard(['/help', '/debug']))
    create_table()
    add_new_user(user_id)

@bot.message_handler(commands=['help'])
def support(message):
    user_id = message.from_user.id
    bot.send_message(user_id,
                     text='Тут есть команды:\n'
                          '/help  помощь\n'
                          '/debug  режим отладчика\n'
                          '/feedback  обратная связь с разработчиком\n',
                     reply_markup=create_keyboard(['/help', '/debug', '/feedback']))
    bot.send_message(user_id,
                     text='Отправь мне текстовое сообщение и я тебе отвечу')

@bot.message_handler(commands=['debug'])
def debug(message):
    with open("logs.txt", "rb") as f:
        bot.send_document(message.chat.id, f)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    user_id = message.from_user.id
    bot.send_message(user_id,
                     text='Скоро здесь появится ссылка на обратную связь',
                     reply_markup=create_keyboard(['/help', '/debug']))

@bot.message_handler(content_types=['text'])
def main(message):
    user_id = message.from_user.id

    if message.content_type != 'text':
        bot.send_message(user_id,
                         text='Нужно отправить именно текстовое сообщение')
        bot.register_next_step_handler(message, main)
        return

    tokens = gpt.count_tokens(message.text)
    if tokens > MAX_TOKENS:
        bot.send_message(user_id,
                         text='Сообщение превышает допустимое количество символов')
        bot.register_next_step_handler(message, main)

    update_tokens(user_id, tokens)
    user_request = message.text

    promt = gpt.make_promt(user_request)
    resp = gpt.send_request(promt)

    answer = gpt.process_resp(response=resp)
    gpt_tokens = gpt.count_tokens(answer[1])
    add_messages(user_id, user_request, tokens, gpt_tokens, answer[1])

    bot.send_message(user_id,
                     text=f'GPT: {answer[1]}',
                     reply_markup=create_keyboard(['Продолжи', 'Завершить ответ']))


bot.polling()

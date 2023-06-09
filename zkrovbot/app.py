from telebot import types, telebot
import json

from dto import base
from poll.anket import anket
from poll.config import questions
from telebot.storage import StateMemoryStorage
from dto.base import DbConnection

import logging

db = DbConnection()
state_storage = StateMemoryStorage()

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot('6057982365:AAGcun8crAp-z6bN0XPtf7ygA6tZr6yQeQo', state_storage=state_storage)


def gen_markup(options, k):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    l = [types.InlineKeyboardButton(x, callback_data=f'{k}_{x}')
         for x in options]
    markup.add(*l)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    req = call.data.split('_')
    k = int(req[0]) + 1
    answer = req[1]
    print(req)
    if k == 0 and answer == "Нет":
        return bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text='На нет и суда нет :)')
    if k > 0:
        db.add_answer(call.from_user.id, k - 1, answer)
    if k == anket.length:
        score = anket.get_score(call.from_user.id)
        return bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text=f'спасибо за ответы, вы набрали: {score} баллов')

    if db.get_type_by_id(k) == 'opened':
        msg = bot.send_message(chat_id=call.message.chat.id, text=anket.get_question(k))
        bot.register_next_step_handler(msg, openaAnswer, k)
    else:
        button_column = db.get_options_by_id(k)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=anket.get_question(k),
                              reply_markup=gen_markup(button_column, k))

    # print(answers)


def openaAnswer(message, k):
    k += 1
    if k == 1:
        print(f"add user {message.text}")
        db.insert_user(message.text, message.from_user.id)
    button_column = db.get_options_by_id(k)
    if db.get_type_by_id(k) == 'opened':
        msg = bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
        bot.register_next_step_handler(msg, openaAnswer, k)
    else:
        bot.send_message(chat_id=message.chat.id, text=anket.get_question(k),
                         reply_markup=gen_markup(button_column, k))


@bot.message_handler(commands=['start'])
def start(message):
    k = -1  # с какого вопроса начинаем опрос
    button_column = ['Да', 'Нет']
    bot.send_message(chat_id=message.chat.id, text="Привет, я бот! Ответь на мои вопросы",
                     reply_markup=gen_markup(button_column, k))


bot.polling()

# -*- coding: utf-8 -*-
import config
import telebot
import leet
import sqlite3 as lite

from random import choice
from random import randint
from telebot import types
from linkparser import LinkHTMLParser
from time import sleep

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['kek'])
def kek(message):
    bot.send_message(message.chat.id, 'kek')

@bot.message_handler(commands=['flood'])
def flood(message):
    smpl = message.text.split(' ')
    try:
        lim = int(smpl[1])
        if(lim<100):
            rus_flood_letters = 'авып'
            for i in range(0, lim):
                ls = ''.join(choice(rus_flood_letters) for i in range(randint(2, 4)))
                bot.send_message(message.chat.id, ls)
                sleep(0.2)
        else:
            bot.send_message(message.chat.id,'Слишком большое количество сообщений. Допускается меньше 100.')
    except:
        bot.send_message(message.chat.id, 'Не могу определить количество. Формат команды: /flood <кол-во сообщений>')

@bot.message_handler(commands=['links'])
def getting_links(message):
    link = message.text.split()[1]
    p = LinkHTMLParser(link)
    bot.send_message(message.chat.id, p.get_links())
    p.__del__()

@bot.message_handler(commands=['leet'])
def leeting(message):
    input_str = message.text[5:]
    bot.send_message(message.chat.id, leet.transformToLeet(input_str))

@bot.message_handler(commands=['game'])
def any_msg(message):
    bot.send_game(message.chat.id, 'FlappyTar')

@bot.callback_query_handler(func=lambda call: True)
def callback_answer (query):
    bot.answer_callback_query(callback_query_id=query.id, url='http://inspiring-easley-168036.bitballoon.com')

@bot.message_handler(commands=['add_phone_number'])
def geophone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Отправить номер телефона в БД ', reply_markup=keyboard)

@bot.inline_handler(func=lambda query: True)
def inline_mode(query):
    capibara1 = types.InlineQueryResultCachedPhoto(
        id="1",
        photo_file_id="AgADAgADq6kxG_UDUEhVQs-boPevsaMLMw4ABJjMgNMwUdhohDAEAAEC",
        caption="ЭНИГМА"
    )
    bot.answer_inline_query(query.id, [capibara1, ])

@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    bot.send_message(message.chat.id, str(message.photo[-1].file_id))
    bot.reply_to(message, 'File has been saved')

if __name__ == '__main__':
    bot.polling(none_stop=True)

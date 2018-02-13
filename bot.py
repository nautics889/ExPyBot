# -*- coding: utf-8 -*-
import config
import telebot
import time
import re
import leet

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
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Flappy Tarasov", url="http://inspiring-easley-168036.bitballoon.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Сыграть в игру...", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
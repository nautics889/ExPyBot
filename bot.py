# -*- coding: utf-8 -*-
import config
import telebot

from random import choice
from random import randint


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['kek'])
def kek(message):
    bot.send_message(message.chat.id, 'kek')

@bot.message_handler(commands=['flood'])
def flood(message):
    smpl = message.text.split(' ')
    try:
        lim = int(smpl[1])
        rus_flood_letters = 'авып'
        for i in range(0, lim):
            ls = ''.join(choice(rus_flood_letters) for i in range(randint(2, 4)))
            bot.send_message(message.chat.id, ls)
    except:
        bot.send_message(message.chat.id, 'Не могу определить количество. Формат команды: /flood <кол-во сообщений>')

if __name__ == '__main__':
    bot.polling(none_stop=True)
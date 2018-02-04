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
    bot.send_message(message.chat.id, 'Сколько?')
    @bot.message_handler(content_types=['text'])
    def flooding(message):
        try:
            len = int(message.text)
            rus_letters = 'авып'
            bot.send_message(message.chat.id, len)
            for i in range(0,len):
                ls = ''.join(choice(rus_letters) for i in range(randint(2,4)))
                bot.send_message(message.chat.id, ls)
        except:
            bot.send_message(message.chat.id, 'Не могу в численный тип данных')

if __name__ == '__main__':
    bot.polling(none_stop=True)
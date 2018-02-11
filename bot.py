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

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, query.query)
    except AttributeError as ex:
        return


    try:
        num1, num2 = matches.group().split()
        m_sum = int(num1) + int(num2)
        r_sum = types.InlineQueryResultArticle(
            id='1', title="Сумма",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description="Результат: {!s}".format(m_sum),
            input_message_content=types.InputTextMessageContent(
                message_text="{!s} + {!s} = {!s}".format(num1, num2, m_sum))
        )
        m_sub = int(num1) - int(num2)
        r_sub = types.InlineQueryResultArticle(
            id='2', title="Разность",
            description="Результат: {!s}".format(m_sub),
            input_message_content=types.InputTextMessageContent(
                message_text="{!s} - {!s} = {!s}".format(num1, num2, m_sub))
        )
        # Учтем деление на ноль и подготовим 2 варианта развития событий
        if num2 is not "0":
            m_div = int(num1) / int(num2)
            r_div = types.InlineQueryResultArticle(
                id='3', title="Частное",
                description="Результат: {0:.2f}".format(m_div),
                input_message_content=types.InputTextMessageContent(
                    message_text="{0!s} / {1!s} = {2:.2f}".format(num1, num2, m_div))
            )
        else:
            r_div = types.InlineQueryResultArticle(
                id='3', title="Частное", description="На ноль делить нельзя!",
                input_message_content=types.InputTextMessageContent(
                    message_text="Я нехороший человек и делю на ноль!")
            )
        m_mul = int(num1) * int(num2)
        r_mul = types.InlineQueryResultArticle(
            id='4', title="Произведение",
            description="Результат: {!s}".format(m_mul),
            input_message_content=types.InputTextMessageContent(
                message_text="{!s} * {!s} = {!s}".format(num1, num2, m_mul))
        )
        bot.answer_inline_query(query.id, [r_sum, r_sub, r_div, r_mul])
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))

if __name__ == '__main__':
    bot.polling(none_stop=True)
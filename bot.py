# -*- coding: utf-8 -*-
import config
import telebot
import time
import requests
import logging
import eventlet

from random import choice
from random import randint
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

def get_data():
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(config.URL_VK)
        return feed.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving VK JSON data. Cancelling...')
        return None
    finally:
        timeout.cancel()

def send_new_posts(items, last_id):
    for item in items:
        if item['id'] <= last_id:
            break
        link = '{!s}{!s}'.format(config.BASE_POST_URL, item['id'])
        bot.send_message(config.CHANNEL_NAME, link)
        # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
        time.sleep(1)
    return

def check_new_posts_vk():
    # Пишем текущее время начала
    logging.info('[VK] Started scanning for new posts')
    with open(config.FILENAME_VK, 'rt') as file:
        last_id = int(file.read())
        if last_id is None:
            logging.error('Could not read from storage. Skipped iteration.')
            return
        logging.info('Last ID (VK) = {!s}'.format(last_id))
    try:
        feed = get_data()
        # Если ранее случился таймаут, пропускаем итерацию. Если всё нормально - парсим посты.
        if feed is not None:
            entries = feed['response'][1:]
            try:
                # Если пост был закреплен, пропускаем его
                tmp = entries[0]['is_pinned']
                # И запускаем отправку сообщений
                send_new_posts(entries[1:], last_id)
            except KeyError:
                send_new_posts(entries, last_id)
            # Записываем новый last_id в файл.
            with open(config.FILENAME_VK, 'wt') as file:
                try:
                    tmp = entries[0]['is_pinned']
                    # Если первый пост - закрепленный, то сохраняем ID второго
                    file.write(str(entries[1]['id']))
                    logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
                except KeyError:
                    file.write(str(entries[0]['id']))
                    logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
    except Exception as ex:
        logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__, str(ex)))
        pass
    logging.info('[VK] Finished scanning')
    return

if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    if not config.SINGLE_RUN:
        while True:
            check_new_posts_vk()
            # Пауза в 4 минуты перед повторной проверкой
            logging.info('[App] Script went to sleep.')
            time.sleep(60 * 4)
    else:
        check_new_posts_vk()
    logging.info('[App] Script exited.\n')
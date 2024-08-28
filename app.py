import json

import telebot
from my_class import search, get_user
from datetime import datetime
import requests

API_TOKEN = ''
AI_KEY = ''
ADMIN = 1855411421
bot = telebot.TeleBot(API_TOKEN, parse_mode='MARKDOWN')
date = datetime(2024, 9, 2)


def get_week():
    return (datetime.today() - date).days // 7 + 1


def get_weekday():
    return datetime.today().isoweekday()


def reply_to_msg(message, data, date):
    if not data:
        bot.reply_to(message, '📅 *%s - %s*\n\n*无课*' % (date['week'], date['weekday']))
    else:
        send = []
        for d in data:
            send.append('```%s【第%s节】 %s\n📍%s```' % (
                d['name'], d['lesson_number'], d['lesson_time'], d['room']))
        bot.reply_to(message, '📅 *%s - %s*\n\n%s' % (
            date['week'], date['weekday'], '\n'.join(send)))


@bot.message_handler(commands=['help', 'start'])
def start(message):
    bot.reply_to(message,
                 '/today - 获取今日课表\n/tomorrow - 获取明日课表\n/get week weekday - 获取指定week星期weekday的课表')


@bot.message_handler(commands=['today'])
def today(message):
    data, date = search(get_week(), get_weekday())
    reply_to_msg(message, data, date)


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    data, date = search(get_week(), get_weekday() + 1)
    reply_to_msg(message, data, date)


@bot.message_handler(regexp='/get *')
def get(message):
    info = message.text.split(' ')
    if len(info) == 2:
        all_data = []
        for r in range(1, 7):
            data, date = search(int(info[-1]), r)
            reply_to_msg(message, data, date)
    else:
        data, date = search(int(info[-2]), int(info[-1]))
        reply_to_msg(message, data, date)


@bot.message_handler(regexp='/ota *')
def ota(message):
    if message.chat.id != ADMIN:
        bot.reply_to(message, 'OTA失败, 不是管理员❌')
    else:
        try:
            req = requests.get(message.text.split(' ')[-1])
        except requests.exceptions.MissingSchema:
            bot.reply_to(message, 'OTA失败, 链接格式有误❌')
        if req.status_code != 200:
            bot.reply_to(message, 'OTA失败, 错误状态码: %s❌' % req.status_code)
        else:
            with open('data.json', 'w', encoding='utf-8') as file:
                file.write(req.text)
            user = get_user()
            bot.reply_to(message, 'OTA成功, 已更换为\n*%s %s\n%s %s(%s)* 的课表✅' % (
                user['department'], user['major'], user['adminclass'], user['name'], user['code']))


@bot.message_handler(func=lambda message: True)
def ai(message):
    data = json.dumps(
        {'model': 'gemini-1.5-pro', "messages": [{"role": "user", "content": message.text}], "max_tokens": 512,
         "stream": False})
    headers = {'content-type': 'application/json', 'Authorization': f"Bearer {AI_KEY}"}
    ai_reply = json.loads(requests.post('https://api.aimlapi.com/chat/completions', headers=headers, data=data).text)
    bot.reply_to(message, ai_reply['choices'][0]['message']['content'])


bot.infinity_polling()

import telebot
from my_class import get_today
import random

API_TOKEN='1871971135:AAFNwRhEX2P-AcQy2AuWtpDMe-SPlha6Ny8'
bot=telebot.TeleBot(API_TOKEN,parse_mode='MARKDOWN')

@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.reply_to(message,'使用 /today 指令获取今日课表')

@bot.message_handler(commands=['today'])
def send_welcome(message):
    td=get_today()
    if td==[]:
    	bot.reply_to(message,'今日无课')
    else:
    	for t in td:
    		bot.reply_to(message,'*%s*的时候, \n记得去`%s%s`, \n上%s老师的`%s`, \n这可是有%s个学分的%s, \n*%s*就下课啦%s'%(t['上课时间'],t['教学楼'],t['教室'],', '.join(t['老师']),t['课程名称'],t['学分'],t['课程类型'],t['下课时间'],random.choice(['👻','👾','😈','🤖','🎃'])))
    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,message.text)

bot.infinity_polling()
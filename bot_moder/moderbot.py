#telegram bot for moderation groups
#bot name:  sahbot
#bot username: mupsah_bot


import telebot
import re
import json
from datetime import datetime, timedelta
from telebot import types
from pprint import pprint # to investigate what inside objects


f = open("token.txt","r")
token = f.readline()
token = token.rstrip() # read about function
print(token, type(token))
f.close()
bot = telebot.TeleBot(token, parse_mode=None)

print(bot.get_me())
print(types.BotCommandScope)
#print(bot.get_chat('@tbros'))
#bot.send_message('@tbros','aaa')

bc = types.BotCommand('lol','lol command')
bc_a = types.BotCommand('fun','anekdot')
bc_q = types.BotCommand('question','ask smt')
bot.set_my_commands([bc,bc_a,bc_q])
#bot.set_my_commands([bc,bc_a,bc_q], types.BotCommandScope())


#types.MenuButtonDefault('default')

# try send message to user


#commands
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, "\U0001F916Добро пожаловать!")
    print('bot.message.form_user.id: '+ str(message.from_user.id))
    print('bot.message.form_user.id: '+ str(message.from_user.id))
    #start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    #start_markup.row('/start', '/help', '/hide')

@bot.message_handler(regexp=".*(хуй|пизд|сука|еба|алуп|ида).*")
def echo_rex(message):
    #bot.send_message(message.chat.id, "Не ругайся!")
    bot.reply_to(message,"ответ наругань")
    print( message.chat.__dir__())
    print( message.chat.__dict__)
    
    #print( bot.get_сhat(message.chat.id)) # 'TeleBot' object has no attribute 'get_сhat'
    print('--- chat.permissions ---')
    print(message.chat.permissions)
    ban_time = datetime.now() + timedelta(hours=0, minutes=3)

    new_perm = types.ChatPermissions(can_send_messages=False)
    print('- New permission -')
    print(new_perm)
    bot.restrict_chat_member(message.chat.id, message.from_user.id, ban_time)
    print("user id:" + str(message.from_user.id))
    #bot.reply_to(message, '''Вы хотите зарегистрировать ЛК!''')

@bot.message_handler(regexp=".*топи.*")
def echo_rex(message):
    bot.reply_to(message, '''Вы хотите узнать ЛС!''')

#regexp example 3
@bot.message_handler(regexp=".*(рикрепи|обавить).*")
def attach_ls(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('send shit'))
    msg = bot.send_message(message.chat.id, "choose type shit", reply_markup=markup)
    

#anything other messages
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    if message.text == 'send shit':
        bot.reply_to(message,'Take shit')

bot.infinity_polling()

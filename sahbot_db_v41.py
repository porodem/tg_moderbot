#telegram bot MUP SAH non-official test
#bot name:  sahbot
#bot username: mupsah_bot


import telebot
import re
from telebot import types
from datetime import datetime

import sqlhelper

icons = {'phone':'\U0000260E','receipt':'U+1F9FE','email':'U+270','money':'\U0001F4B0',
         'calendar':'U+1F4C6','bin':'U+1F6AE','warning':'U+26A0',
         'eco':'U+267B','check':'U+2714','cross':'\U0000274C','green_circle':'\U0001F7E2',
         'computer':'\U0001F4BB'}

bot = telebot.TeleBot("", parse_mode=None)


bc_start = types.BotCommand('start','Начать диалог с ботом')
bc_getls = types.BotCommand('getls','Узнать лицевой счет')
bc_contacts = types.BotCommand('contacts','Контакты')
bot.set_my_commands([bc_start,bc_getls,bc_contacts])
#bot.set_my_commands([bc,bc_a,bc_q], types.BotCommandScope())



#types.MenuButtonDefault('default')

#commands
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(types.KeyboardButton(icons['green_circle'] + ' Узнать ЛС'))
    markup.add(types.KeyboardButton(icons['computer'] +' Вопрос по личному кабинету'))
    markup.add(types.KeyboardButton(icons['money'] + ' Вопрос по оплате'))
    msg = bot.send_message(message.chat.id, "Какой у Вас вопрос?", reply_markup=markup)
    #log
    log_file = open('botlog.txt','a')
    req_date = datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
    log_file.write('\n' + str(req_date) + ' ' + message.from_user.first_name + ' ' + str(message.from_user.last_name or ''))
    log_file.close()

@bot.message_handler(commands=['getls','contacts'])
def ls_or_contacts(message):
    if message.text == '/getls':
        ls_fork(message)
    else:
        more_contacts(message)

#process main questions

def get_ls(message):
    print('get_ls function. msg= ' + message.text)
    print('user: ' + message.from_user.first_name)
    if message.text == 'Нет':
        #3rd argument for remove buttons from ls_fork(message) function
        bot.send_message(message.from_user.id, 'Тогда вам нужно найти номер на сайте.',reply_markup=types.ReplyKeyboardRemove())
        print('get_ls end')
    elif message.text == 'Да':
        bot.send_message(message.from_user.id, '''Введите Улицу, дом, квартиру через запятые.\n
Например: Владимировская, 3, 1''')
        bot.register_next_step_handler(message, ask_db_ls)

def ask_db_ls(message): # use input address from person to get LS from DB
    if re.match('.*,.*,.*',message.text):
        person_ls = sqlhelper.get_ls_from_db(message.text)
        bot.reply_to(message,person_ls)
    else:
        message.text = 'Да'
        get_ls(message)
    

@bot.message_handler(regexp=".*" + icons['green_circle'] + ".*")
def ls_fork(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Да'))
    markup.add(types.KeyboardButton('Нет'))
    bot.send_message(message.chat.id, "Вы проживете в г. Новосибирск?", reply_markup=markup)
    bot.register_next_step_handler(message, get_ls)


#Inline handler (action for press inline buttons)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yess": #call.data it's callback_data which we add when initialise button
        #code for saving or processing data
        bot.send_message(call.message.chat.id, 'Got it!')
    elif call.data == "noo":
        bot.send_message(call.message.chat.id, 'oh no!')



@bot.message_handler(regexp=".*(ператор|человек|алоб).*")
def more_contacts(message):
    bot.reply_to(message, '''Вы можете подать обращение на сайте мупсах.рф.
Кроме того cообщить о переполнении контейнеров ТКО, а также оставить заявку на вывоз КГО и РСО можно по номеру телефона ДИСПЕТЧЕРСКОЙ СЛУЖБЫ: 363 - 04 - 22
Вопросы, связанные с начислениями и оплатой услуги по обращению ТКО, можно задать по номеру телефона АБОНЕНТСКОЙ СЛУЖБЫ: 363 - 04 - 11
Наши операторы принимают звонки потребителей с 8:00 до 20:00 ежедневно''')

@bot.message_handler(regexp=".*(латить|лат[а|е]).*")
def pay_question(message):
    bot.reply_to(message, '''Совершить оплату можно с помощью:
- Личного кабинета https://lk.cax54.ru
- Приложения Платосфера
- Квартплата+
- приложение Сбербанк
Вопросы, связанные с начислениями и оплатой услуги по обращению ТКО, можно задать по номеру телефона АБОНЕНТСКОЙ СЛУЖБЫ: 363 - 04 - 11
Наши операторы принимают звонки потребителей с 8:00 до 20:00 ежедневно''')

@bot.message_handler(regexp=".*(абинет|ичный|айте).*")
def site_account(message):
    bot.reply_to(message, '''Кажется вы хотите зарегистрировать личный кабинет на сайте?
Если так, пожалуйста, пройтите по ссылке https://lk.cax54.ru/client/login
Скоро мне добавят функцию и я смогу вам отправлять инструкцию работе в ЛК!''')

@bot.message_handler(regexp=".*ицевой.*")
def echo_rex(message):
    #bot.reply_to(message, '''Хотите узнать новый ЛС в МУП САХ?''')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(icons['green_circle'] + ' Узнать мой ЛС'))
    markup.add(types.KeyboardButton('Открепиь ЛС от ЛК'))
    msg = bot.send_message(message.chat.id, "Какой у Вас вопрос по поводу лицевого счета?", reply_markup=markup)



#regexp example 3
@bot.message_handler(regexp=".*(рикрепи|обавить).*")
def attach_ls(message):
    bot.reply_to(message,'''Прикрепить ЛС можно в личном кабинете. Для этого войдите или зарегистрируйтесь
зарегистрируйтесь на сайте мупсах.рф - в разделе Личный кабинет. Прямая ссылка: https://lk.cax54.ru/''')
    

#anything other messages
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    """Send file to user"""
    if message.text == 'File':
        file = open('C:\Python\Python310\Scripts\sahbot\инструкция ЛК САХ.pdf','rb')
        msg = bot.send_document(message.chat.id,file)
        doc_id = msg.document.file_id #this file_id only for learning purposes
        # file once being loaded better handle by this ID, not downloading it' anytime it's needed
        # if we work not with document, but photo or audio etc. principe is the same
        print('file_id: ' + doc_id)
    elif message.text == 'мой ЛС':
        bot.reply_to(message,'Here your new LS')
    else:
        bot.reply_to(message,'Простите, я Вас непонял. Пожалуйста, попробуйте ещё раз или воспользуйтесь кнопкой "Меню".')

#example of inline
@bot.message_handler(commands=['xxx','yyy'])
def test_welcome(message):
    bot.reply_to(message, "\U0001F916Добро пожаловать!")
    #Inline Keyboards (don't send msg to the chat)
    k_btn = types.InlineKeyboardButton(text='iLbtn', callback_data='yess')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(k_btn)
    #show lnline keyboard in bot's chat
    bot.send_message(message.from_user.id, text="select", reply_markup=keyboard)
    #start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    #start_markup.row('/start', '/help', '/hide')

bot.infinity_polling()


    

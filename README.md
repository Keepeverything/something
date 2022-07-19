# something
# -*- coding: utf-8 -*-
import telebot
import urllib
import time
from telebot import types
import os, json, logging, sys

token = '1763846034:AAE9NADn4uDfnPUfKnuKNQrEA-EG3HmnsJ8'
bot = telebot.TeleBot(token, threaded=False)

users = {}

f = open('psyqes.txt',encoding='utf-8')
q = eval(f.read())


@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda msg: msg.text == 'Пройти тест еще раз')
def send_welcome(message):
    #print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    strategy = types.KeyboardButton('Пройти тест еще раз')
    
    if message.chat.id not in users:
        users[message.chat.id] = {'state':0,'score':0}
    markup.row(strategy)

    bot.send_message(message.chat.id, '''Укажите *ФИО* и номер группы''',parse_mode = 'Markdown',  reply_markup=markup)





@bot.message_handler(content_types=["text"])
def content_text(message):
    if message.chat.id not in users:
        users[message.chat.id] = {'state':0,'score':0}
    print(message.text)
    #print(q[users[message.chat.id]['state']]['buttons'])
    if not users[message.chat.id]['state'] == 0:
        users[message.chat.id]['score'] = users[message.chat.id]['score'] + q[users[message.chat.id]['state']]['buttons'][message.text]
    users[message.chat.id]['state'] = users[message.chat.id]['state'] + 1
    btn = []
    for i in q[users[message.chat.id]['state']]['buttons']:
        btn.append(types.KeyboardButton(i))

    #settings = VkApi.add_button(text='Настройки', payload='settings', color='positive')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(btn)==2:
        keyboard.row(btn[0],btn[1])
        print (users[message.chat.id]['score'])
    else:
        keyboard.row(btn[0],btn[1],btn[2])
        print (users[message.chat.id]['score'])

    if message.text != '':
        if users[message.chat.id]['state'] == 1:
            bot.send_message(message.chat.id, 'Окей начнем!')
        bot.send_message(message.chat.id, q[users[message.chat.id]['state']]['name'], reply_markup=keyboard, parse_mode = 'Markdown')

    if users[message.chat.id]['state'] == 71:
        time.sleep(5)
        users[message.chat.id]['score'] = users[message.chat.id]['score'] + q[users[message.chat.id]['state']]['buttons'][message.text]
        bot.send_message(message.chat.id, '''*Итак ваш результат*''')
        if users[message.chat.id]['score'] < 16:
            bot.send_message(message.chat.id,'Ваш уровень напряжения близок к нулевой отметке. Такой результат может говорить о том, что вы либо уделили вопросам недостаточно внимания, либо вы крайне плохо осознаете происходящие с вами процессы. Рекомендуем вам пройти опросник позднее повторно более внимательно или обратиться за консультацией к психологу.')
        elif users[message.chat.id]['score'] < 45 and users[message.chat.id]['score'] > 16:
            bot.send_message(message.chat.id,"У вас хорошие адаптивные возможности. Ваша психика успешно справляется с требованиями окружающей среды. Вы способны контролировать эмоциональное состояние в разнообразных условиях. В то же время, если вы все же чувствуете внутреннюю неудовлетворенность происходящим в вашей жизни, пожалуйста обратите должное внимание на это ощущение. На индивидуальной консультации с психологом вы всегда можете поделиться любыми происходящими внутри вас процессами.")
        elif users[message.chat.id]['score'] < 60 and users[message.chat.id]['score'] > 45:
            bot.send_message(message.chat.id,"Ваш уровень стресса высокий, однако вы в состоянии контролировать напряжение. Вы способны обратить внимание на свое состояние и понять причину своих эмоциональных реакций. Свойства вашей нервной системы позволяют сохранять приемлемую работоспособность. Однако высокий уровень напряжения истощает и, в какой-то момент чаша может оказаться переполненной. Вероятно, вам не хватает знаний и навыков для полноговладения своим психическим состоянием в ряде ситуаций. Такие навыки вы можете приобрести на специальных психологических тренингах, а также на индивидуальных консультациях с психологом.")
        elif users[message.chat.id]['score'] > 59:
            bot.send_message(message.chat.id,"Ваша нервная система испытывает чрезмерные нагрузки. Ваш уровень стресса сильно завышен. Ваш уровень осознанности очень низкий, что не позволяет вам понять истинных причин постоянного напряжения, а также управлять собственным состоянием. Постоянное напряжение вызывает также сложности во взаимодействии с другими, зачастую не позволяет принять поддержку или попросить о ней, что только подливает масла в огонь. Вам требуется психологическая поддержка, а ваше эмоциональное состояние требует немедленной корректировки.")
        test = types.KeyboardButton('Пройти тест еще раз')

    test = types.ReplyKeyboardMarkup(resize_keyboard=True)    
    test.row(types.KeyboardButton('Пройти тест еще раз'))
    users[message.chat.id] = {'state':0,'score':0}
    bot.send_message(message.chat.id, 'Если хочешь пройти тест еще раз нажми на кнопку', reply_markup=test, parse_mode = 'Markdown')
        

@bot.message_handler()
def all(message):

    bot.send_message(message.chat.id, 'gg wp')
     

while True:
    try:
        bot.polling()    
    except Exception as e:
        #bot.send_message(410754290, e)
        print(e)
        time.sleep(3)
    print('lol')
    time.sleep(3)

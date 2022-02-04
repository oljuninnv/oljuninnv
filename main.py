import telebot
from telebot import TeleBot
import random
import sqlite3
from parserc import Parser
import pymorphy2


morph = pymorphy2.MorphAnalyzer(lang='ru')
db = sqlite3.connect('users.db', check_same_thread=False)

emoji = ['😡','😍','😦','','','','','','','','','','','','']

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(chat_id integer primary key, name text, age integer, sex text)")

bot = TeleBot("5063426005:AAFy7JdUcpge9fl8HAXswO7RpIZ5QODiwsc")
@bot.message_handler(commands=['start'])
def hello_message(message):
    name = bot.send_message(message.chat.id,"Приветик,как тебя зовут?")
    bot.register_next_step_handler(name,SetUserName)
    

def SetUserName(message):
    cursor.execute('INSERT OR REPLACE INTO users(chat_id, name, age, sex) VALUES(?,?,?,?)', (message.chat.id, message.text, None, None))
    db.commit()
    age = bot.send_message(message.chat.id, f'Я тебя запомнила {message.text}. Укажи свой возраст')
    bot.register_next_step_handler(age,SetUserAge)

    

def SetUserAge(message):
    cursor.execute(f'UPDATE users  SET age =? WHERE chat_id=?', (message.text, message.chat.id))
    db.commit()
    sex = bot.send_message(message.chat.id, f'хорошо!,Укажи свой пол')
    bot.register_next_step_handler(sex,SetUserSex)

def SetUserSex(message):
    cursor.execute(f'UPDATE users  SET sex =? WHERE chat_id=?', (message.text, message.chat.id))
    db.commit()
    bot.send_message(message.chat.id, f'всё спасибо :)')



@bot.message_handler(content_types=['text'])
def message_handler(message):
    print(message)
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_message(message.chat.id,random.choice(['я тебя тоже','ня :)','пасибки']))
    elif message.text.lower() in ['приветик','привет','шалом']:
        bot.send_message(message.chat.id, random.choice(['ПРИВЕТ','ПРИВЕТИК','ХАЙ','ОНИЧАН']))
    elif message.text.lower() in ['как дела','как дела?','как жизнь','как жизнь?']:
        msg = bot.send_message(message.chat.id,"Хорошо, а у тебя?")
        bot.register_next_step_handler(msg, dela_2)
    elif message.text.lower().startswith('температура утром в'):
        city = message.text.lower()[20:]
        city = morph.parse(city)[0].normal_form
        parser = Parser(f'https://sinoptik.com.ru/погода-{city}')
        weather = parser.get_texts(container = 'div', c_class='table__temp', elements=8)
        bot.send_message(message.chat.id,f'Лови братик {weather[0]}')
    elif message.text.lower().startswith('температура днём в'):
        city = message.text.lower()[19:]
        city = morph.parse(city)[0].normal_form
        parser = Parser(f'https://sinoptik.com.ru/погода-{city}')
        weather = parser.get_texts(container = 'div', c_class='table__temp', elements=8)
        bot.send_message(message.chat.id,f'Надеюсь ты скоро разберёшься с делами{weather[2]}')
            
    elif message.text.lower().startswith('температура вечером в'):
        city = message.text.lower()[22:]
        city = morph.parse(city)[0].normal_form
        parser = Parser(f'https://sinoptik.com.ru/погода-{city}')
        weather = parser.get_texts(container = 'div', c_class='table__temp', elements=8)
        bot.send_message(message.chat.id,f'Возвращайся лучше поскорее {weather[4]}')
    elif message.text.lower().startswith('температура ночью в'):
        city = message.text.lower()[20:]
        city = morph.parse(city)[0].normal_form
        parser = Parser(f'https://sinoptik.com.ru/погода-{city}')
        weather = parser.get_texts(container = 'div', c_class='table__temp', elements=8)
        bot.send_message(message.chat.id,f'Лучше поспи и никуда не иди {weather[6]}')
    elif message.text.lower() in ['хочешь шутку','хочешь прикол','внимание анекдот']:
        msg = bot.send_message(message.chat.id,'ОООООО ДАВАЙ')
        bot.register_next_step_handler(msg,joke)

@bot.message_handler(content_types=["sticker"])
def send_sticker(message):
    sticker_id = message
    
    if message.sticker.emoji == "😤":
        msg=bot.send_message(message.chat.id,'узбагойся,что случилось?')
        bot.register_next_step_handler(msg,dela_3)
    print(sticker_id.sticker.emoji)

def joke(message):
    if message != '':
        bot.send_message(message.chat.id,random.choice(['АХХХАХАХ','Смешная шутка','хихиххиих']))
    else:
        return

def dela_2(message):
    if message.text.lower() in ['норм','отлично','хорошо','заебись','ахуено','топ','пиздато']:
        bot.send_message(message.chat.id,'Рада за тебя :)')
    elif message.text.lower() in ['ужасно','плохо','хуёво','так себе','не очень']:
        a=bot.send_message(message.chat.id,'Блин, а что случилось :(')
        bot.register_next_step_handler(a,dela_3)

def dela_3(message):
    if message.text.lower() in ['не хочу об этом говорить','не хочу это обсуждать']:
        bot.send_message(message.chat.id,'Ну ладно....')
    else:
        bot.send_message(message.chat.id,'Надеюсь всё наладится')



print('Бот запущен')
bot.infinity_polling()
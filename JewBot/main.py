from email import message
from telebot import TeleBot
import random
from bs4 import BeautifulSoup as bs
import sqlite3
import table


db = sqlite3.connect("info",check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS price(магазин TEXT NOT NULL,название товара TEXT NOT NULL,изображение BLOB NOT NULL,цена  REAL)")



bot=TeleBot("5011274028:AAEFBdvKwLLaK5sWbsSXTvfWH2MrutTQiIg")
@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id,'Шалом')

@bot.message_handler(content_types=['text'])
def talk_message(message):
    if message.text.lower() in ['привет','здаров']:
        bot.send_message(message.chat.id,'Таки вздравствуй')
    




print('Бот запущен')
bot.infinity_polling()
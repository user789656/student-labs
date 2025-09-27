from telebot import TeleBot, types
import requests
import datetime
import os
from dotenv import load_dotenv
"""
Для работы бота:
    -запусти python BestBot.py
Для отключения:
    -ctrl + c
"""
load_dotenv()
TOKEN = os.getenv('TOKEN')
BOSS_CHAT_ID = int(os.getenv('BOSS_CHAT_ID'))
URL = 'https://api.thecatapi.com/v1/images/search'
bot = TeleBot(token=TOKEN)


def is_boss(CHAT_ID):
    return CHAT_ID == BOSS_CHAT_ID


def get_new_image(CHAT_ID):
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    bot.send_photo(CHAT_ID,  random_cat)


def get_current_time(CHAT_ID):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    bot.send_message(chat_id=CHAT_ID, text=current_time)


def salutation(CHAT_ID):
    if is_boss(CHAT_ID):
        ANSWER = 'Здравствуй, создатель!'
    else:
        ANSWER = 'Здравствуй, человек!'
    bot.send_message(chat_id=CHAT_ID, text=ANSWER)


@bot.message_handler(commands=['start'])
def wake_up(message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('Привет'),
        types.KeyboardButton('Котика, пожалуйста'),
    )
    keyboard.row(
        types.KeyboardButton('Сколько времени?'),
    )

    CHAT_ID = message.chat.id
    BOT_NAME = bot.get_me().first_name
    bot.send_message(chat_id=CHAT_ID,
                     text=f'{BOT_NAME} активирован!',
                     reply_markup=keyboard)


@bot.message_handler(commands=['котика, пожалуйста'])
def new_cat(message):
    get_new_image(message.chat.id)


@bot.message_handler(content_types=['text'])
def answer_to_boss(message):
    CHAT_ID = message.chat.id
    TEXT = message.text.lower()
    for i in ['привет', 'здравствуй', 'hello', 'hi']:
        if i in TEXT:
            salutation(CHAT_ID)
    for i in ['дай мне котика', 'я хочу котика', 'котика, пожалуйста']:
        if i in TEXT:
            get_new_image(CHAT_ID)
    if 'сколько времени' in TEXT:
        get_current_time(CHAT_ID)


def main():
    bot.polling()


if __name__ == '__main__':
    main()

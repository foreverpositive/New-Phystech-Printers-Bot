import logging
import telebot
from datetime import datetime


with open('TOKEN.secret', 'r', encoding='utf-8') as file:
    TOKEN = file.readline()

bot = telebot.TeleBot(TOKEN, parse_mode=None)
user = bot.get_me()
LANG = "English"


@bot.message_handler(commands=['start'])
def send_welcome(message, language=LANG):
    chat_id = message.chat.id
    sender_id = message.from_user.id
    sender_fullname = message.from_user.full_name

    bot.send_message(chat_id, f"Hello, {sender_fullname}!")

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton("English")
    itembtn2 = telebot.types.KeyboardButton("Russian")
    markup.add(itembtn1, itembtn2)
    bot.send_message(chat_id, "Please choose the language:", reply_markup=markup)
    bot.register_next_step_handler(message, set_language)


def set_language(message):
    global LANG
    LANG = message.text
    bot.send_message(message.chat.id, f"Language have been successfully chosen! ({LANG})")
    send_instructions(message)


def send_instructions(message):
    chat_id = message.chat.id
    with open('instruction.jpg', 'rb') as file:
        instruction_pic = file.read()

    bot.send_photo(chat_id, instruction_pic)
    bot.send_message(chat_id, f"Are you first time here? If so, please paste your Telegram ID to your profile in https://physics.itmo.ru/")


@bot.message_handler(commands=['help'])
def send_help(message, language=LANG):
    help_info = """This is a bot that helps faculty members of New Phystech work with faculty's public printers. Here you can easily choose a method of printing, which data will be printed with selected printer."""
    chat_id = message.chat.id
    bot.send_message(chat_id, help_info)


bot.infinity_polling()

import csv
import telebot

logger = telebot.logging.getLogger()
telebot.logging.basicConfig(filename="logs/bot.log",
                            datefmt='%d-%m-%Y %H:%M:%S',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='a+', encoding='utf-8',
                            level=telebot.logging.DEBUG)

with open('TOKEN.secret', 'r', encoding='utf-8') as token_file:
    TOKEN = token_file.readline()

bot = telebot.TeleBot(TOKEN, parse_mode=None)
LANG = "English"

phrases = {}
with open('phrases.csv', 'r', encoding='utf-8') as phrases_file:
    reader = csv.reader(phrases_file)
    for row in reader:
        phrases[row[0]] = {'English': row[1], 'Русский': row[2]}


@bot.message_handler(commands=['start'])
def send_welcome(message, language=LANG):
    chat_id = message.chat.id
    sender_fullname = message.from_user.full_name

    hello_str = phrases['hello'][language].format(sender_fullname)
    sent_msg = bot.send_message(chat_id, hello_str)

    change_language(sent_msg)

    bot.register_next_step_handler(sent_msg, send_instructions)


def set_language(message):
    global LANG

    chat_id = message.chat.id

    if message.text in ('English', 'Русский'):
        LANG = message.text[:]
        lang_chosen_str = phrases['lang_chosen'][LANG]
        bot.send_message(chat_id, lang_chosen_str)
        logger.info('Successfully changed language')
    else:
        wrong_lang_str = phrases['wrong_lang'][LANG]
        bot.send_message(chat_id, wrong_lang_str)
        logger.error('Wrong language choice')


@bot.message_handler(commands=['language'])
def change_language(message, language=LANG):
    chat_id = message.chat.id

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               one_time_keyboard=True,
                                               resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton("English")
    itembtn2 = telebot.types.KeyboardButton("Русский")
    markup.add(itembtn1, itembtn2)
    choose_lang_str = phrases['choose_lang'][language]

    sent_choice = bot.send_message(chat_id, choose_lang_str, reply_markup=markup)

    bot.register_next_step_handler(sent_choice, set_language)
    logger.info('Waiting for input')


def send_instructions(message, language=LANG):
    chat_id = message.chat.id
    user_id = message.from_user.id

    with open('instruction.jpg', 'rb') as instr_pic_file:
        instruction_pic = instr_pic_file.read()

    bot.send_photo(chat_id, instruction_pic)
    instr_str = phrases['instruction'][language].format(user_id)
    bot.send_message(chat_id, instr_str)
    logger.info("Sent instructions")


@bot.message_handler(commands=['help'])
def send_help(message, language=LANG):
    help_str = phrases['help'][language]
    chat_id = message.chat.id
    bot.send_message(chat_id, help_str)
    logger.info("Sent help")


bot.infinity_polling()

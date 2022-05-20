import os
import telebot
from translations import translations
from members import is_member

token = os.environ['BOT_TOKEN']
# with open('bot/bot-token', 'r', encoding='utf-8') as token_file:
#     token = token_file.readline()


logger = telebot.logging.getLogger()
telebot.logging.basicConfig(filename="logs/bot.log",
                            datefmt='%d-%m-%Y %H:%M:%S',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='a+',
                            encoding='utf-8',
                            level=telebot.logging.DEBUG)

telebot.apihelper.ENABLE_MIDDLEWARE = True

MAIN_STATE = 'ON_MAIN_MENU'
CHANGE_LANG = 'ON_LANG_MENU'
SET_PRINTER = 'ON_PRINTER_MENU'
NEW_PRINT = 'ON_PRINTING_MENU'
SESSIONS = {}
TRANSLATIONS = translations.load_tr()

_lang = 'en'


def activate(lang):
    global _lang
    _lang = lang


def tr(string):
    """Returns string respectively to language"""
    try:
        return TRANSLATIONS[string][_lang]
    except KeyError as e:
        logger.error('%e: %s is not in TRANSLATIONS', e, string)
        translations.json_from_csv()
        try:
            tr_str = TRANSLATIONS[string][_lang]
            logger.info('%s found in TRANSLATIONS after regenerating', string)
            return tr_str
        except KeyError as ee:
            logger.fatal(
                '%e: %s is not in TRANSLATIONS after regenerating file', ee, string)
            return tr('not_tr')


def get_or_create_session(user_id):
    try:
        return SESSIONS[user_id]
    except KeyError:
        SESSIONS[user_id] = {'state': MAIN_STATE}
        SESSIONS[user_id] = {'lang': 'en'}
        return SESSIONS[user_id]


bot = telebot.TeleBot(token, parse_mode=None)


@bot.middleware_handler(update_types=['message'])
def set_session(bot_instance, message):
    bot_instance.session = get_or_create_session(message.from_user.id)


@bot.middleware_handler(update_types=['message'])
def activate_language(bot_instance, message):
    lang = message.from_user.language_code
    SESSIONS['lang'] = lang
    activate(lang)


def not_member(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    sent_msg = bot.send_message(chat_id, tr('not_member'))
    bot.register_next_step_handler(sent_msg, send_instructions(message))
    logger.info("Access denied to user %s", user_id)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    bot.session['state'] = MAIN_STATE

    sender_fullname = message.from_user.full_name
    bot.send_message(chat_id, tr('hello').format(sender_fullname))

    choose_language(message)
    send_instructions(message)


@bot.message_handler(commands=['language'])
def choose_language(message):
    bot.session['state'] = CHANGE_LANG

    user_id = message.from_user.id
    chat_id = message.chat.id

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               one_time_keyboard=True,
                                               resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton("English")
    itembtn2 = telebot.types.KeyboardButton("Русский")
    markup.add(itembtn1, itembtn2)

    sent_markup = bot.send_message(chat_id, tr('choose_lang'), reply_markup=markup)

    bot.register_next_step_handler(sent_markup, set_language)
    logger.info('Waiting for language input')


def set_language(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text in ('English', 'Русский'):
        bot.session['lang'] = message.text
        msg = bot.send_message(chat_id, tr('lang_chosen'))
        logger.info('Successfully changed lang to %s', message.text)
    else:
        msg = bot.send_message(chat_id, tr('wrong_lang'))
        bot.register_next_step_handler(msg, choose_language(message))
        logger.error('Wrong language choice')


def send_instructions(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    with open('src/instruction.jpg', 'rb') as instr_pic_file:
        instruction_pic = instr_pic_file.read()

    bot.send_photo(chat_id, instruction_pic)
    bot.send_message(chat_id, tr('instruction').format(user_id))
    logger.info("Sent instructions")


@bot.message_handler(commands=['help'])
def send_help(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    bot.send_message(chat_id, tr('help'))
    logger.info("Sent help")


@bot.message_handler(commands=['printer'])
def choose_printer(message):
    bot.session['state'] = SET_PRINTER

    user_id = message.from_user.id
    chat_id = message.chat.id

    if not is_member(user_id):
        not_member(message)
        return

    markup = telebot.types.ReplyKeyboardMarkup(row_width=3,
                                               one_time_keyboard=True,
                                               resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton("Entrance")
    itembtn2 = telebot.types.KeyboardButton("Coffee")
    itembtn3 = telebot.types.KeyboardButton("Library")
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(chat_id, tr('choose_printer'), reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(chat_id, set_printer)


def set_printer(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not is_member(user_id):
        not_member(message)
        return

    if message.text in ('Entrance', 'Coffee', 'Library'):
        bot.session['printer'] = message.text
        bot.send_message(chat_id, tr('printer_chosen'))
        logger.info('Successfully set printer (%s)', message.text)
    else:
        bot.send_message(chat_id, tr('wrong_printer'))
        bot.register_next_step_handler_by_chat_id(
            chat_id, choose_printer(message))
        logger.error('Wrong printer choice')


bot.infinity_polling()

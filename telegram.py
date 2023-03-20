import telebot
from telebot import types
from chatbot import getResponse
from aiml_bot import getAimlResponse
from check_language import checkIsRussian, checkIsEnglish

bot = telebot.TeleBot('5807632118:AAGTEY5tZcDYUW72H7NXFpsIy2BmCiF83ms')


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

def getBtn4():
    return types.KeyboardButton("🧭Sklearn модель (Русский)" if isAIML else "🧭AIML модель (Английский)")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⛅Какая погода?")
    btn2 = types.KeyboardButton("⏱️Сколько время?")
    btn3 = types.KeyboardButton("💿 Жесткие диски")
    markup.add(btn1, btn2, btn3)

    markup.add(getBtn4())

    if message.text == '👋 Поздороваться':
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)
        return True

    is_russian = checkIsRussian(message.text)
    is_english = checkIsEnglish(message.text)

    if not is_russian and not is_english:
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос на русском или английском языке', reply_markup=markup)
        return True

    if is_english:
        bot.send_message(message.from_user.id, getAimlResponse(message.text), reply_markup=markup)
        return True

    response = getResponse(message.text)

    try:
        if response[1] & response[1] == 'advertisement':
            goods_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_disk = types.KeyboardButton("💿 Список жестких дисков")
            goods_markup.add(btn_disk)
            bot.send_message(message.from_user.id, response[0], reply_markup=goods_markup)
            return True
    except Exception:
        bot.send_message(message.from_user.id, response[0], reply_markup=markup)
        return True

    bot.send_message(message.from_user.id, response[0], reply_markup=markup)


bot.polling(none_stop=True, interval=0)
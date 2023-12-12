import telebot
from telebot import types

API_TOKEN = '6648168132:AAHAo2Yym4oVmiHfj_zOtWY2jJXDpzkQdB4'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    wb_button = types.KeyboardButton("WB")
    ozon_button = types.KeyboardButton("OZON")
    markup.row(wb_button, ozon_button)
    bot.send_message(message.chat.id, 'Сделай выбор:', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'WB':
        bot.send_message(message.chat.id, 'Введите ссылку')
    elif message.text == 'OZON':
        bot.send_message(message.chat.id, 'Введите ссылку')
    bot.register_next_step_handler(message, handle_link)


@bot.message_handler(regexp=r'^https?://')
def handle_link(message):
    link = message.text
    bot.send_message(message.chat.id, f"Вы отправили ссылку: {link}")


bot.infinity_polling()
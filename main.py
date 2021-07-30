import telebot
import config
import time

answers = ['привет', 'пока', 'как дела', 'какое сегодня число', 'сколько времени']

bot = telebot.TeleBot(config.key)

def main_kb():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Меню', callback_data="menu")
    keyboard.add(button)
    return keyboard

def kb():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_date = telebot.types.InlineKeyboardButton(text='Дата', callback_data="date")
    button_time = telebot.types.InlineKeyboardButton(text='Время', callback_data="time")
    keyboard.add(button_date, button_time)
    return keyboard

@bot.message_handler(content_types=["text"])
def f(message):
    t = time.ctime(time.time()).split()
    mess = message.text.lower()
    if mess[-1] == '?':
        mess = mess[:-1]
    ans = ''
    if mess == answers[0] or mess == '/start':
        ans = 'Привет'
    elif mess == answers[1]:
        ans = 'До свидания'
    else:
        ans = 'не понимаю'

    bot.send_message(message.chat.id, ans, reply_markup=main_kb())

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    if call.message:
        t = time.ctime(time.time()).split()
        if call.data == "menu":
            ans = 'Главное меню'
        elif call.data == "date":
            ans = 'Сегодняшнее число: ' + t[2] + ' ' + t[1] + ' ' + t[4]
        elif call.data == "time":
            ans = 'Текущее время: ' + t[3]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=ans, reply_markup=kb())


if __name__ == '__main__':
    bot.infinity_polling()
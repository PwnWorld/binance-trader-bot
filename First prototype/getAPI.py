#CopyRight Cod3rman
#Contact : instagram.com/root_ahor4
#Telegam Auto Trader Bot version:1.1.0

import telebot
import mpu.io
import os
import json
import re
from telebot import types

f = open("telegram_api.conf", "r")
bot = telebot.TeleBot(f.read().split()[0])
# bot = telebot.TeleBot("YOUR Telegram API Key")

key = ""  # MUST BE len() 64
secret = ""  # MUST BE len() 64

data = {}


@bot.message_handler(content_types=["text"])
def hello_user(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton("/start")
    itembtnb = types.KeyboardButton("/reg")
    markup.row(itembtna, itembtnb)
    bot.send_message(
        message.from_user.id,
        "Hello: " + str(message.from_user.username),
        reply_markup=markup,
    )
    if doesFileExists("%s.json" % message.from_user.id):

        global data
        global key
        global secret

        with open("%s.json" % message.from_user.id, "r") as read_file:
            data = json.load(read_file)
            key = data["key"]
            secret = data["secret"]

        bot.send_message(message.from_user.id, "Yaa config file it exists!")
        bot.send_message(message.from_user.id, "Key is: " + key)
        bot.send_message(message.from_user.id, "Secret is: " + secret)
    else:
        bot.send_message(
            message.from_user.id, "Nope! I don't find config file, lets create one..."
        )
        bot.send_message(message.from_user.id, "Type /reg")
        bot.register_next_step_handler(message, start)


def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)


def start(message):
    if message.text == "/reg":
        bot.send_message(message.from_user.id, "Enter Binance API KEY:")
        bot.register_next_step_handler(message, get_key)
    else:
        bot.send_message(message.from_user.id, "Type /reg")


def get_key(message):
    global key
    if len(message.text) == 64:
        key = message.text
        bot.send_message(message.from_user.id, "Enter Binance API Secret:")
        bot.register_next_step_handler(message, get_secret)
    else:
        bot.send_message(message.from_user.id, "Wrong API KEY, type /reg again !")


def get_secret(message):
    global secret
    if len(message.text) == 64:
        secret = message.text
        bot.send_message(message.from_user.id, "ID is: " + str(message.from_user.id))
        bot.send_message(message.from_user.id, "Key is: " + key)
        bot.send_message(message.from_user.id, "Secret is: " + secret)
        data = {"key": key, "secret": secret}
        mpu.io.write("%s.json" % message.from_user.id, data)
    else:
        bot.send_message(message.from_user.id, "Wrong API SECRET, type /reg again !")



bot.polling(none_stop=True, interval=1)

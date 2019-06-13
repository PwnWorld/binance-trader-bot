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

signals_data = None

pair = None  # MUST BE LIKE BNBBTC
# MUST BE FLOAT 0.12345678
buy = None
stop_loss = None
sell_1 = None
sell_2 = None
sell_3 = None
sell_4 = None
sell_5 = None


@bot.message_handler(content_types=["text"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton("/start")
    markup.row(itembtna)
    bot.send_message(
        message.from_user.id, "Forward signal message to me ...", reply_markup=markup
    )

    if message.text == "/start":
        bot.register_next_step_handler(message, get_forward)
    else:
        bot.send_message(message.from_user.id, "Type /start")


def get_forward(message):
    global signals_data
    global pair
    global buy
    global stop_loss
    global sell_1
    global sell_2
    global sell_3
    global sell_4
    global sell_5

    signals_data = message.text

    pair_pos_start = signals_data.find("#")
    pair_pos_end = signals_data.find("BTC")
    sdd = signals_data[pair_pos_start:pair_pos_end]
    pair = re.sub(r"[^A-Za-z]", "", sdd) + "BTC"

    buy_pos_start = signals_data.find("Покупка")
    buy_tmp = re.findall(r"[-+]?\d*\.\d+|\d+", (signals_data[buy_pos_start:]))[0]
    total = 10000000
    buy = float("0." + str(buy_tmp).zfill(len(str(total))))

    stop_loss_pos_start = signals_data.find("Стоп")
    stop_loss_tmp = re.findall(
        r"[-+]?\d*\.\d+|\d+", (signals_data[stop_loss_pos_start:])
    )[0]
    total = 10000000
    stop_loss = float("0." + str(stop_loss_tmp).zfill(len(str(total))))

    sell_pos_start = signals_data.find("Цели")
    until_stop_loss_pos = signals_data.find("Стоп")
    sell_tmp = re.findall(
        r"[-+]?\d*\.\d+|\d+", (signals_data[sell_pos_start:until_stop_loss_pos])
    )
    if len(sell_tmp) == 5:
        total = 10000000
        sell_1 = float("0." + str(sell_tmp[0]).zfill(len(str(total))))
        sell_2 = float("0." + str(sell_tmp[1]).zfill(len(str(total))))
        sell_3 = float("0." + str(sell_tmp[2]).zfill(len(str(total))))
        sell_4 = float("0." + str(sell_tmp[3]).zfill(len(str(total))))
        sell_5 = float("0." + str(sell_tmp[4]).zfill(len(str(total))))
    elif len(sell_tmp) == 4:
        total = 10000000
        sell_1 = float("0." + str(sell_tmp[0]).zfill(len(str(total))))
        sell_2 = float("0." + str(sell_tmp[1]).zfill(len(str(total))))
        sell_3 = float("0." + str(sell_tmp[2]).zfill(len(str(total))))
        sell_4 = float("0." + str(sell_tmp[3]).zfill(len(str(total))))
        sell_5 = None
    elif len(sell_tmp) == 3:
        total = 10000000
        sell_1 = float("0." + str(sell_tmp[0]).zfill(len(str(total))))
        sell_2 = float("0." + str(sell_tmp[1]).zfill(len(str(total))))
        sell_3 = float("0." + str(sell_tmp[2]).zfill(len(str(total))))
        sell_4 = None
        sell_5 = None
    elif len(sell_tmp) == 2:
        total = 10000000
        sell_1 = float("0." + str(sell_tmp[0]).zfill(len(str(total))))
        sell_2 = float("0." + str(sell_tmp[1]).zfill(len(str(total))))
        sell_3 = None
        sell_4 = None
        sell_5 = None
    elif len(sell_tmp) == 1:
        total = 10000000
        sell_1 = float("0." + str(sell_tmp[0]).zfill(len(str(total))))
        sell_2 = None
        sell_3 = None
        sell_4 = None
        sell_5 = None

    bot.send_message(message.from_user.id, "Done")
    bot.send_message(message.from_user.id, "Pair is: " + str(pair))
    bot.send_message(message.from_user.id, "Buy is: " + str(buy))
    bot.send_message(message.from_user.id, "Stop_loss is: " + str(stop_loss))
    bot.send_message(message.from_user.id, "Sell 1 is: " + str(sell_1))
    bot.send_message(message.from_user.id, "Sell 2 is: " + str(sell_2))
    bot.send_message(message.from_user.id, "Sell 3 is: " + str(sell_3))
    bot.send_message(message.from_user.id, "Sell 4 is: " + str(sell_4))
    bot.send_message(message.from_user.id, "Sell 5 is: " + str(sell_5))


bot.polling(none_stop=True, interval=1)

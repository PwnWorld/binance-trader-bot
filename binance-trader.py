#CopyRight Cod3rman
#Contact : instagram.com/root_ahor4
#Telegam Auto Trader Bot version:1.1.0
import telebot
import mpu.io
import os
import sys
import json
import re
from telebot import types
import ccxt
import time
from time import sleep
from numbers import Number

f = open("telegram_api.conf", "r")
bot = telebot.TeleBot(f.read().split()[0])

exchange = None
key = ""
secret = ""
exchange_fee = 0.1
data = {}

signals_data = None
pair = None
coin = None
buy = None
sdd = None
stop_loss = None
sell_1 = None
sell_2 = None
sell_3 = None
sell_4 = None
sell_5 = None
amount = None
selected_sell_target = None
balance_btc = None
balance_coin = None
buy_after_exchange_fee = None
orders_executed = []

example_signal_post = "#BTG Binance\n\nBuy 311200\n\nTargets:\n\n391100\n491100\n591100\n691100\n791100\n\nStop loss 221100"


@bot.message_handler(content_types=["text"])
def hello_user(message):

    global example_signal_post

    bot.send_message(
        message.from_user.id,
        "Hi "
        + str(message.from_user.username)
        + "\n"
	+ "-->If you have any Problem Tell me from this ID : @Cod3r_man"
	+ "\n"
        + "-->If you need reboot me - send /restart",
	+ "\n"
	+ "---Join ITRoadMap channel to get news and updates---"

    )
    bot.send_message(
        message.from_user.id,
        "Bellow example post with signal\nYou should forward post to me it is same format only!\n",
    )
    bot.send_message(message.from_user.id, example_signal_post)

    if doesFileExists("%s.json" % message.from_user.id):
        with open("%s.json" % message.from_user.id, "r") as read_file:

            global data
            global key
            global secret
            global exchange

            data = json.load(read_file)
            key = data["key"]
            secret = data["secret"]
            exchange = ccxt.binance(
                {"apiKey": key, "secret": secret, "enableRateLimit": True}
            )
            bot.send_message(
                message.from_user.id, "Forward message with signals to me ..."
            )
            bot.register_next_step_handler(message, get_forward)

    else:
        bot.send_message(
            message.from_user.id, "I don't find Your account, let's create one ..."
        )
        bot.send_message(message.from_user.id, "Enter Exchange API KEY:")
        bot.register_next_step_handler(message, get_key)


def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)


def get_key(message):

    global key

    if message.text == "/restart":
        restart_bot(message)

    elif len(message.text) == 64:
        key = message.text
        bot.send_message(message.from_user.id, "Enter Exchange SECRET KEY:")
        bot.register_next_step_handler(message, get_secret)
    else:
        bot.send_message(message.from_user.id, "Wrong API KEY! Check and try again.")
        bot.register_next_step_handler(message, get_key)


def get_secret(message):

    global secret
    global exchange

    if message.text == "/restart":
        restart_bot(message)

    elif len(message.text) == 64:
        secret = message.text

        bot.send_message(
            message.from_user.id,
            "Yeah, Your account is created, forward message with signals to me ...",
        )
        bot.register_next_step_handler(message, get_forward)
        data = {"key": key, "secret": secret}
        mpu.io.write("%s.json" % message.from_user.id, data)
        exchange = ccxt.binance(
            {"apiKey": key, "secret": secret, "enableRateLimit": True}
        )
    else:
        bot.send_message(message.from_user.id, "Wrong API SECRET! Check and try again.")
        bot.register_next_step_handler(message, get_secret)


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
    global exchange
    global sdd

    signals_data = message.text

    if (len(str(signals_data)) >= 50) or (message.text == "/restart"):
        if message.text == "/restart":
            restart_bot(message)
        pair_pos_start = signals_data.find("#")
        pair_pos_end = signals_data.find(" ")
        sdd = signals_data[pair_pos_start:pair_pos_end]
        pair = re.sub(r"[^A-Za-z]", "", sdd) + "/BTC"

        buy_pos_start = signals_data.find("Buy")
        buy_tmp = re.findall(r"[-+]?\d*\.\d+|\d+", (signals_data[buy_pos_start:]))[0]
        total = 10000000
        buy = float("0." + str(buy_tmp).zfill(len(str(total))))

        stop_loss_pos_start = signals_data.find("Stop loss")
        stop_loss_tmp = re.findall(
            r"[-+]?\d*\.\d+|\d+", (signals_data[stop_loss_pos_start:])
        )[0]
        total = 10000000
        stop_loss = float("0." + str(stop_loss_tmp).zfill(len(str(total))))

        sell_pos_start = signals_data.find("Targets")
        until_stop_loss_pos = signals_data.find("Stop loss")
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

        bot.send_message(message.from_user.id, "Signals received, look like:")
        bot.send_message(message.from_user.id, "Pair: " + str(pair))
        bot.send_message(message.from_user.id, "Buy: " + str(buy))
        bot.send_message(message.from_user.id, "Stop-loss: " + str(stop_loss))

        if sell_1 is not None:
            bot.send_message(message.from_user.id, "Sell target 1: " + str(sell_1))
        if sell_2 is not None:
            bot.send_message(message.from_user.id, "Sell target 2: " + str(sell_2))
        if sell_3 is not None:
            bot.send_message(message.from_user.id, "Sell target 3: " + str(sell_3))
        if sell_4 is not None:
            bot.send_message(message.from_user.id, "Sell target 4: " + str(sell_4))
        if sell_5 is not None:
            bot.send_message(message.from_user.id, "Sell target 5: " + str(sell_5))

        bot.send_message(message.from_user.id, "What target do we will use? ")
        bot.register_next_step_handler(message, select_sell)

    else:
        bot.send_message(
            message.from_user.id, "Don't typing to me! Forward message only."
        )
        bot.register_next_step_handler(message, get_forward)


def select_sell(message):

    global sell_1
    global sell_2
    global sell_3
    global sell_4
    global sell_5
    global selected_sell_target
    global balance_coin
    global balance_btc
    global coin

    if (
        (message.text == "1" and sell_1 is not None)
        or (message.text == "2" and sell_2 is not None)
        or (message.text == "3" and sell_3 is not None)
        or (message.text == "4" and sell_4 is not None)
        or (message.text == "5" and sell_5 is not None)
        or (message.text == "/restart")
    ):
        if message.text == "1":
            selected_sell_target = sell_1
        elif message.text == "2":
            selected_sell_target = sell_2
        elif message.text == "3":
            selected_sell_target = sell_3
        elif message.text == "4":
            selected_sell_target = sell_4
        elif message.text == "5":
            selected_sell_target = sell_5
        elif message.text == "/restart":
            restart_bot(message)

        bot.send_message(
            message.from_user.id, "Selected sell target: " + str(selected_sell_target)
        )

        coin = re.sub(r"[^A-Za-z]", "", sdd)
        balance_fetch = exchange.fetch_balance()
        balance_coin = float(balance_fetch["free"][coin])
        bot.send_message(
            message.from_user.id, "Your " + coin + " balance: " + str(balance_coin)
        )

        balance_btc = float(balance_fetch["free"]["BTC"])

        bot.send_message(
            message.from_user.id, "Your BTC balance: " + str(balance_btc) + " "
        )
        bot.send_message(
            message.from_user.id,
            "What percent from your balance will I use for this trade?\nType number, 10 for example.",
        )
        bot.register_next_step_handler(message, get_amount)

    else:
        bot.send_message(message.from_user.id, "Type number ONLY! ")
        bot.register_next_step_handler(message, select_sell)


def get_amount(message):

    global amount
    global balance_coin
    global balance_btc
    global buy_after_exchange_fee
    global coin

    min_trade_amount = 10 / exchange.fetch_ticker("BTC/USDT")["low"]

    try:
        amount = (float(balance_btc) / 100) * float(message.text)
        if amount <= balance_btc and amount > 0:
            if amount > min_trade_amount:
                buy_after_exchange_fee = (amount / buy) - (
                    ((amount / buy) / 100) * exchange_fee
                )  # Fee in coin
                bot.send_message(
                    message.from_user.id,
                    "In this trade I will use " + str(amount) + " BTC",
                )
                bot.send_message(
                    message.from_user.id,
                    "For them we will receive "
                    + str(buy_after_exchange_fee)[:10]
                    + " "
                    + coin,
                )
                bot.send_message(message.from_user.id, "If you agree, type YES")
                bot.register_next_step_handler(message, trader)
            else:
                bot.send_message(
                    message.from_user.id,
                    "You want to use"
                    + " "
                    + str(amount)
                    + " BTC\n"
                    + "but minimal trade amount "
                    + str(min_trade_amount)[:8]
                    + " BTC! ~$10",
                )
                bot.register_next_step_handler(message, get_amount)

        else:
            bot.send_message(message.from_user.id, "It is bigger than your BTC balance")
            bot.register_next_step_handler(message, get_amount)

    except:
        bot.send_message(message.from_user.id, "Enter correct percent (number only!)")
        bot.register_next_step_handler(message, get_amount)


def trader(message):

    if message.text == "/restart":
        restart_bot(message)
    elif message.text == "YES":
        bot.send_message(message.from_user.id, "Placing buy order ...")
        buy_order(message)
        bot.register_next_step_handler(message, buy_order)
    else:
        bot.send_message(message.from_user.id, "Just send me YES")
        bot.register_next_step_handler(message, trader)


def buy_order(message):

    global amount
    global pair
    global buy
    global exchange
    global orders_executed
    global buy_order_fee

    type = "limit"
    side = "buy"
    amount_to_buy_exchange = amount / buy
    params = {}

    buy_order = exchange.create_order(
        pair, type, side, amount_to_buy_exchange, buy, params
    )
    orders_executed.append(buy_order["id"])

    bot.send_message(
        message.from_user.id,
        "I placed buy order, I will notify you when it will executed ...",
    )
    check_order_status_and_sell(message)
    bot.register_next_step_handler(message, check_order_status_and_sell)


def check_order_status_and_sell(message):

    while True:

        global orders_executed
        global pair
        global exchange

        params = {}

        if exchange.fetchOrder(orders_executed[0], pair, params)["status"] == "closed":
            bot.send_message(
                message.from_user.id, "Buy order is executed, preparing selling ..."
            )
            sell_order(message)
            bot.register_next_step_handler(message, sell_order)
            break
        else:
            pass
            buy_order_status = exchange.fetchOrder(orders_executed[0], pair, params)[
                "status"
            ]
            bot.send_message(
                message.from_user.id, "Waiting for buy order execution ..."
            )
            time.sleep(30)


def sell_order(message):

    global pair
    global exchange
    global orders_executed
    global selected_sell_target
    global stop_loss
    global buy_after_exchange_fee

    buy_after_exchange_fee = float(str(buy_after_exchange_fee)[:10])

    stop_loss_limit_order = exchange.create_order(
        pair,
        "stop_loss_limit",
        "sell",
        buy_after_exchange_fee,
        selected_sell_target,
        {"stopPrice": stop_loss},
    )
    bot.send_message(message.from_user.id, "Sell order placed, I wish You Profit :)")
    bot.send_message(
        message.from_user.id, "For use my services again, send me /start :)"
    )

    os.execl(sys.executable, sys.executable, *sys.argv)


def restart_bot(message):

    if message.text == "/restart":
        bot.send_message(message.from_user.id, "Restart complete, send me /start")
        os.execl(sys.executable, sys.executable, *sys.argv)


bot.polling(none_stop=True, interval=0)

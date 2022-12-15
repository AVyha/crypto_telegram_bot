import random

from dotenv import load_dotenv
import os

import telebot
import requests
from bs4 import BeautifulSoup


load_dotenv()

bot = telebot.TeleBot(
    os.environ.get("BOT_TOKEN"), parse_mode=None
)

URL = "https://paper-trader.frwd.one"


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Write trading pair."
    )


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    context = {
        "pair": message.text,
        "timeframe": random.choice(["5m", "15m", "1h", "4h", "1d", "1w", "1M"]),
        "candles": random.randint(0, 1000),
        "ma": random.randint(0, 100),
        "tp": random.randint(0, 100),
        "sl": random.randint(0, 100),
    }

    page = requests.post(URL, context).content
    soup = BeautifulSoup(page, "html.parser")

    try:
        image = soup.select_one("img")["src"]

        bot.send_photo(message.chat.id, URL + image[1:])

        response_msg = "Your data is: \n"
        for keys in context:
            response_msg += f"{keys} - {context[keys]} \n"

        bot.reply_to(message, response_msg)
    except (TypeError, UnboundLocalError):
        bot.reply_to(message, "Invalid pair!")


bot.infinity_polling()

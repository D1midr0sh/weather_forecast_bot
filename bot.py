import logging
import os

import api_handler

from dotenv import load_dotenv

import telebot
from telebot.types import Message

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start_message(message):
    msg = "Привет, я погодный бот. Напиши мне название города и я расскажу погоду."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=["text"])
def get_weather(message: Message) -> None:
    city_name = message.text
    try:
        new_message = api_handler.get_message(city_name)
    except Exception as e:
        logging.critical(e)
        bot.send_message(message.chat.id, "Произошла какая-то ошибка. Напиши ещё раз.")
    bot.send_message(message.chat.id, new_message)


if __name__ == "__main__":
    bot.polling(non_stop=True)

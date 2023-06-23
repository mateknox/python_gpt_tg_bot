import sources
import telebot
import logging
import config
import random

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    logging.info(f"Got a start msg: ${message}")
    msg = "Available commands: \n" \
          "/genre Film genre \n" \
          "/gpt Anything \n" \
          "/help \n" \
          "/start"
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['genre'])
def omdb_message(message):
    logging.info(f"Got an omdb msg: ${message}")
    description = message.text[message.text.find(" "):].lstrip()
    msg = sources.get_info_from_omdb(description)
    logging.info("Got info from omdb:")
    random.shuffle(msg)
    logging.info(msg[0:6])
    final_msg = 'No info found'
    for elem in msg[0:6]:
        elem = elem.split("/")[2]
        elem_info = sources.get_info_from_omdb(elem)
        if ("title" and "image") in elem_info:
            final_msg = "Film: " + elem_info["title"] + "\n" + "Poster: " + elem_info["image"]["url"] + "\n"
        # if there is no description
        elif "title" in elem:
            final_msg = "Film: " + elem["title"] + "\n" + "There is no poster" + "\n"
    bot.send_message(message.chat.id, final_msg, parse_mode='Markdown')


@bot.message_handler(commands=['gpt'])
def gpt_message(message):
    logging.info(f"Got an gpt msg: ${message}")
    description = message.text[message.text.find(" "):].lstrip()
    msg = sources.get_info_from_gpt(description)
    logging.info(f"Got info from gpt: ${msg}")
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(True)

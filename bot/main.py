import sources
import telebot
import logging
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    logging.info(f"Got start msg: ${message}")
    msg = "Available commands: \n" \
          "/genre Film genre \n" \
          "/gpt Anything \n" \
          "/help \n" \
          "/start"
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['genre'])
def omdb_message(message):
    logging.info(f"Got omdb msg: ${message}")
    description = message.text[message.text.find(" "):].lstrip()
    msg = sources.get_titles_from_omdb(description)
    random.shuffle(msg)
    logging.info(f"Got titles from omdb: ${msg[0:6]}")
    final_msg = 'No info found'
    for elem in msg[0:6]:
        elem = elem.split("/")[2]
        elem_info = sources.get_info_from_omdb(elem)
        logging.info(f"Film info from omdb: ${elem_info}")
        if ("title" and "image") in elem_info:
            final_msg = "Film: " + elem_info["title"] + "\n" + "Poster: " + elem_info["image"]["url"] + "\n"
        # if there is no description
        elif "title" in elem:
            final_msg = "Film: " + elem["title"] + "\n" + "There is no poster" + "\n"
        bot.send_message(message.chat.id, final_msg, parse_mode='Markdown')


@bot.message_handler(commands=['gpt'])
def gpt_message(message):
    logging.info(f"Got gpt query: ${message}")
    description = message.text[message.text.find(" "):].lstrip()
    gpt_info = gpt_method(description)
    bot.send_message(message.chat.id, gpt_info, parse_mode='Markdown')


@bot.inline_handler(lambda query: '/gpt' in query.query)
def gpt_inline_message(inline_query):
    logging.info(f"Got gpt inline query: ${inline_query}")
    description = inline_query.query[inline_query.query.find(" "):].lstrip()
    try:
        gpt_info = gpt_method(description)
        r = types.InlineQueryResultArticle('1', 'Gpt result', types.InputTextMessageContent(gpt_info))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        logging.error(f"Exception: ${e}")


def gpt_method(description):
    msg = sources.get_info_from_gpt(description)
    logging.info(f"Got info from gpt: ${msg}")
    return msg


if __name__ == '__main__':
    bot.polling(True)

import sources
import telepot
from flask import request, Flask
import logging
import requests
import config
import json
import random

TelegramBot = telepot.Bot(config.TOKEN)
app = Flask(__name__)


# main endpoint
@app.route('/', methods=["GET", "POST"])
def update():
    if request.method == "POST" and "message" in request.json:
        logging.info("Got POST:")
        logging.info(request.json)
        user_text = request.json["message"]["text"]
        chat_id = request.json["message"]["from"]["id"]
        # Response for start message
        if user_text.split(" ")[0] == "/start":
            msg = "Привет! Для поиска фильма доступны следующие команды: /kp, /google, /imdb и /genre" + "\n" + \
                  "В случае с kp и imdb для поиска используются ключевые слова из описания фильма, " \
                  "с google можно искать что угодно, но вернутся 5 первых результатов. Genre возвращает 3 случайных " \
                  "фильма в заданном жанре из списка топ фильмов в данном жанре. " + "\n" + \
                  "Итоговый формат команд: /источник описание. Для повторного вызова списка " \
                  "команд напиши /help или /start."
            send_message(chat_id, msg)

        # Response for help message
        elif user_text.split(" ")[0] == "/help":
            msg = "Для поиска фильма доступны следующие команды: /kp, /google, /imdb и /genre" + "\n" + \
                  "В случае с kp и imdb для поиска используются ключевые слова из описания фильма, " \
                  "с google можно искать что угодно, но вернутся 5 первых результатов. Genre возвращает 3 случайных " \
                  "фильма в заданном жанре из списка топ фильмов в данном жанре. " \
                  "Итоговый формат команд: /источник описание."
            send_message(chat_id, msg)

        # Response for main messages
        elif user_text.split(" ")[0] == "/kp":
            source = "Kinopoisk"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from KP:")
            logging.info(msg)
            for elem in msg["films"][0:5]:
                if ("nameRu" and "description") in elem:
                    final_msg = "Фильм: " + elem["nameRu"] + "\n" + "Описание: " + elem[
                        "description"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "nameRu" in elem:
                    final_msg = "Фильм: " + elem["nameRu"] + "\n" + "Описание отсутствует" + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/google":
            source = "Google"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from Google:")
            logging.info(msg)
            for elem in msg["results"][0:5]:
                if "link" and "description" in elem:
                    final_msg = "Описание: " + elem["description"] + "\n" + "Ссылка: " + elem[
                        "link"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "link" in elem:
                    final_msg = "Ссылка: " + elem["link"] + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/imdb":
            source = "Imdb"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from imdb:")
            logging.info(msg)
            for elem in msg["results"][0:5]:
                if ("title" and "description") in elem:
                    final_msg = "Фильм: " + elem["title"] + "\n" + "Описание: " + elem[
                        "description"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "title" in elem:
                    final_msg = "Фильм: " + elem["title"] + "\n" + "Описание отсутствует" + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/genre":
            source = "Omdb"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from omdb:")
            random.shuffle(msg)
            logging.info(msg[0:3])
            for elem in msg[0:3]:
                elem = elem.split("/")[2]
                elem_info = sources.get_info_from_omdb(elem)
                if ("title" and "image") in elem_info:
                    final_msg = "Фильм: " + elem_info["title"] + "\n" + "Постер: " + elem_info[
                        "image"]["url"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "title" in elem:
                    final_msg = "Фильм: " + elem["title"] + "\n" + "Постер отсутствует" + "\n"
                    send_message(chat_id, final_msg)

        # unknown message
        elif ("/start" or "/help" or "/kp" or "/google" or "/imdb" or "/genre") not in user_text:
            logging.info(user_text)
            msg = "Неизвестная команда, напиши /help для получения списка доступных"
            send_message(chat_id, msg)

    # inline example
    elif request.method == "POST" and "inline_query" in request.json and "query" in request.json["inline_query"]:
        logging.info("Got POST:")
        logging.info(request.json)
        query = request.json["inline_query"]["query"]
        chat_id = request.json["inline_query"]["id"]
        if ("/help" or "/imdb" or "/google" or "/kp") in request.json["inline_query"]["query"]:
            if query == "/help":
                msg = "Для поиска фильма доступы 3 команды: /kp, /google или /imdb" + "\n" + \
                      "В случае с kp и imdb для поиска используются ключевые слова из описания фильма, " \
                      "с google можно искать что угодно, но вернутся 5 первых результатов. " \
                      "Итоговый формат команд: /источник описание."
                send_message_inline(chat_id, msg)
        return "ok"
    return "ok"


# send message to user
def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{config.TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


# send message to user inline
def send_message_inline(chat_id, text):
    method = "answerInlineQuery"
    url = f"https://api.telegram.org/bot{config.TOKEN}/{method}"
    result = [{'type': 'article',
               'title': 'Result',
               'parse_mode': 'Markdown',
               'id': chat_id+'/0',
               'description': text,
               'message_text': text}]
    data = {"inline_query_id": chat_id, "results": json.dumps(result)}
    requests.post(url, data=data)


def main(source, desc):
    if source == "Kinopoisk":
        return sources.get_info_from_kp(desc=desc)
    if source == "Google":
        return sources.get_info_from_google(desc=desc)
    if source == "Imdb":
        return sources.get_info_from_imdb(desc=desc)
    if source == "Omdb":
        return sources.get_titles_from_omdb(desc=desc)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5007')
    logging.info("App is running")

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
            msg = "Available commands: /kp, /google, /imdb и /genre" + "\n" + \
                  "/kp Film description" \
                  "/imdb Film description" \
                  "/google Film description" \
                  "/genre Film genre" \
                  "/help" \
                  "/start"
            send_message(chat_id, msg)

        # Response for help message
        elif user_text.split(" ")[0] == "/help":
            msg = "Available commands: /kp, /google, /imdb и /genre" + "\n" + \
                  "/kp Film description" \
                  "/imdb Film description" \
                  "/google Film description" \
                  "/genre Film genre" \
                  "/help" \
                  "/start"
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
                    final_msg = "Film: " + elem["nameRu"] + "\n" + "Description: " + elem["description"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "nameRu" in elem:
                    final_msg = "Film: " + elem["nameRu"] + "\n" + "There is no description" + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/google":
            source = "Google"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from Google:")
            logging.info(msg)
            for elem in msg["results"][0:5]:
                if "link" and "description" in elem:
                    final_msg = "Description: " + elem["description"] + "\n" + "Link: " + elem["link"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "link" in elem:
                    final_msg = "Link: " + elem["link"] + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/imdb":
            source = "Imdb"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from imdb:")
            logging.info(msg)
            for elem in msg["results"][0:5]:
                if ("title" and "description") in elem:
                    final_msg = "Film: " + elem["title"] + "\n" + "Description: " + elem["description"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "title" in elem:
                    final_msg = "Film: " + elem["title"] + "\n" + "There is no description" + "\n"
                    send_message(chat_id, final_msg)

        elif user_text.split(" ")[0] == "/genre":
            source = "Omdb"
            description = user_text[user_text.find(" "):].lstrip()
            msg = main(source, description)
            logging.info("Got info from omdb:")
            random.shuffle(msg)
            logging.info(msg[0:6])
            for elem in msg[0:6]:
                elem = elem.split("/")[2]
                elem_info = sources.get_info_from_omdb(elem)
                if ("title" and "image") in elem_info:
                    final_msg = "Film: " + elem_info["title"] + "\n" + "Poster: " + elem_info["image"]["url"] + "\n"
                    send_message(chat_id, final_msg)
                # if there is no description
                elif "title" in elem:
                    final_msg = "Film: " + elem["title"] + "\n" + "There is no poster" + "\n"
                    send_message(chat_id, final_msg)

        # unknown message
        elif ("/start" or "/help" or "/kp" or "/google" or "/imdb" or "/genre") not in user_text:
            logging.info(user_text)
            msg = "Unknown command, try /help"
            send_message(chat_id, msg)

    # inline example
    elif request.method == "POST" and "inline_query" in request.json and "query" in request.json["inline_query"]:
        logging.info("Got POST:")
        logging.info(request.json)
        query = request.json["inline_query"]["query"]
        chat_id = request.json["inline_query"]["id"]
        if ("/help" or "/imdb" or "/google" or "/kp") in request.json["inline_query"]["query"]:
            if query == "/help":
                msg = "Available commands: /kp, /google, /imdb и /genre" + "\n" + \
                      "/kp Film description" \
                      "/imdb Film description" \
                      "/google Film description" \
                      "/genre Film genre" \
                      "/help" \
                      "/start"
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

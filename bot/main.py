import sources
import telepot
from flask import request, Flask
import logging
import requests
import config
import random

TelegramBot = telepot.Bot(config.TOKEN)
app = Flask(__name__)


# main endpoint
@app.route('/', methods=["GET", "POST"])
def update():
    if request.method == "POST" and "message" in request.json:
        chat_id = request.json["message"]["from"]["id"]
        try:
            logging.info("Got POST:")
            logging.info(request.json)
            user_text = request.json["message"]["text"]
            # Response for start message
            if user_text.split(" ")[0] == "/start":
                msg = "Available commands: \n" \
                      "/genre Film genre \n" \
                      "/gpt Anything \n" \
                      "/help \n" \
                      "/start"
                send_message(chat_id, msg)

            # Response for help message
            elif user_text.split(" ")[0] == "/help":
                msg = "Available commands: \n" \
                      "/genre Film genre \n" \
                      "/gpt Anything \n" \
                      "/help \n" \
                      "/start"
                send_message(chat_id, msg)

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

            elif user_text.split(" ")[0] == "/gpt":
                source = "Gpt"
                description = user_text[user_text.find(" "):].lstrip()
                msg = main(source, description)
                logging.info("Got info from gpt: ")
                send_message(chat_id, msg)

            # unknown message
            elif ("/start" or "/help" or "/genre") not in user_text:
                logging.info(user_text)
                msg = "Unknown command, try /help"
                send_message(chat_id, msg)

            return ""
        except Exception as e:
            logging.info(f"Exception: ${e}")
            send_message(chat_id, "Error occurred, probably need to add description to command.")
            return ""
    return ""


# send message to user
def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{config.TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def main(source, desc):
    if source == "Omdb":
        return sources.get_titles_from_omdb(desc=desc)
    if source == "Gpt":
        return sources.get_info_from_gpt(message=desc)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5007')
    logging.info("App is running")

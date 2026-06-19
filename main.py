import logging
import random
import telebot
from telebot import types
import config
from sources import MediaSearchEngine

logger = logging.getLogger("media_bot")
bot = telebot.TeleBot(config.TOKEN)

# Single source of truth instance
engine = MediaSearchEngine()


def send_split_message(chat_id, text, parse_mode='Markdown'):
    """Splits text cleanly by paragraphs to avoid breaking Markdown entities across chunks."""
    MAX_LENGTH = 4000  # Safe Telegram limit buffer

    if len(text) <= MAX_LENGTH:
        try:
            bot.send_message(chat_id, text, parse_mode=parse_mode)
            return
        except telebot.apihelper.ApiTelegramException as e:
            logger.warning(f"Single message Markdown parse failed, sending as plain text: {e}")
            bot.send_message(chat_id, text)
            return

    # Split by natural line breaks or paragraphs
    paragraphs = text.split('\n')
    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:
        # Account for the newline character we'll add back when joining
        paragraph_len = len(paragraph) + 1

        # If adding this paragraph exceeds the limit, ship the current chunk
        if current_length + paragraph_len > MAX_LENGTH:
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                try:
                    bot.send_message(chat_id, chunk_text, parse_mode=parse_mode)
                except telebot.apihelper.ApiTelegramException as e:
                    logger.warning(f"Chunk Markdown parse failed, sending as plain text: {e}")
                    bot.send_message(chat_id, chunk_text)

            # Reset trackers for the next message block
            current_chunk = [paragraph]
            current_length = paragraph_len
        else:
            current_chunk.append(paragraph)
            current_length += paragraph_len

    # Send any remaining paragraphs left in the buffer
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        try:
            bot.send_message(chat_id, chunk_text, parse_mode=parse_mode)
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(chat_id, chunk_text)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    msg = (
        "🤖 *Welcome!*\n\n"
        "🎬 `/genre <name>` - Find items by genre\n"
        "🧠 `/gpt <prompt>` - Talk to Gemini\n"
    )
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['genre'])
def genre_handler(message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "⚠️ Provide a genre. Example: `/genre action`")
        return

    genre_query = parts[1].strip()
    raw_titles = engine.search_movies_by_genre(genre_query)

    if not raw_titles:
        bot.send_message(message.chat.id, "❌ No data returned.")
        return

    random.shuffle(raw_titles)

    # Process matches safely safely avoiding array splitter assumptions
    sent_count = 0
    for structural_item in raw_titles:
        if sent_count >= 5:
            break

        # Clean lookups extracting alphanumeric IMDb IDs (ttXXXXX)
        clean_segments = [seg for seg in structural_item.split("/") if seg]
        if not clean_segments:
            continue
        title_id = clean_segments[-1]

        info = engine.get_movie_details(title_id)
        if not info or "title" not in info:
            continue

        title = info["title"]
        # Safe extraction out of optional nested image dictionary fields
        poster_url = info.get("image", {}).get("url")

        if poster_url:
            caption = f"🎬 *Film:* {title}\n🖼️ [Poster Link]({poster_url})"
        else:
            caption = f"🎬 *Film:* {title}\n_No poster available_"

        bot.send_message(message.chat.id, caption, parse_mode='Markdown')
        sent_count += 1


@bot.message_handler(commands=['gpt'])
def gpt_handler(message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "⚠️ Provide a question.")
        return

    ai_response = engine.ask_gemini(parts[1].strip())

    # Use our new splitting logic here instead of direct bot.send_message
    send_split_message(message.chat.id, ai_response, parse_mode='Markdown')


if __name__ == '__main__':
    logger.info("Bot execution loop starting...")
    bot.infinity_polling()

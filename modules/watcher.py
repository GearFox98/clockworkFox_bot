import logging
import os
from datetime import datetime
from telegram import chat, update
from telegram.ext import (Updater,
                        MessageHandler,
                        ConversationHandler)

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )
LOGGER = logging.getLogger()

GUARDIAN = '645812555'#os.getenv('guardian')
def whoami(update, context):
  update.message.reply_text(text = f"{update.effective_user.id}")

def watcher(update, context):
    bot = context.bot

    print(f"your {GUARDIAN}")
    #Chat details
    ID = update.message.chat_id
    GN = update.message.chat.title
    UI = update.effective_user.id
    FN = update.effective_user.first_name
    UN = update.effective_user.username

    try:
      update.message.forward(chat_id = GUARDIAN)
      bot.send_message(
        chat_id = GUARDIAN,
        parse_mode = 'HTML',
        text = f"{ID} - <b>{GN}</b> | {UI} - {FN} - {UN}"
      )
    except Exception as e:
      bot.send_message(
        chat_id = GUARDIAN,
        parse_mode = 'HTML',
        text = f"Error, but: {ID} - <b>{GN}</b> | {UI} - {FN} - {UN}"
      )
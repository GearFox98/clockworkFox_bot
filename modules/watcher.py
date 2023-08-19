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

GUARDIAN = os.getenv('GUARDIAN')
GUARDED = os.getenv('GUARDED')
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
  
    if ID < 0:
      AI = [adm_id.user.id for adm_id in context.bot.get_chat_administrators(ID)]
      AF = [adm_id.user.first_name for adm_id in context.bot.get_chat_administrators(ID)]
      AL = ""

      for i in range(0, len(AI)):
        AL += f"{AI[i]} - {AF[i]} :: "
      
      try:
        update.message.forward(chat_id = GUARDIAN)
        bot.send_message(
          chat_id = GUARDIAN,
          parse_mode = 'HTML',
          text = f"{ID} - <b>{GN}</b> | {UI} - {FN} - {UN} | ADM: {AL}"
        )
      except Exception as e:
        bot.send_message(
          chat_id = GUARDIAN,
          parse_mode = 'HTML',
          text = f"Error, but: {ID} - <b>{GN}</b> | {UI} - {FN} - {UN}"
        )

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import modules.clockworkLib.rhandler as rh
import modules.clockworkLib.fshandler as fh
import modules.clockworkLib.words as words

from wsgiref.util import request_uri
from telegram.ext import (Updater,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          CallbackContext,
                          MessageHandler,
                          Filters)

from telegram import (chat,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton)

from modules import (welcoming,
                     farewell,
                     secretFriend,
                     raffle)

#Server
PORT = int(os.environ.get('PORT', '8443'))

#Token
TOKEN = os.environ['TOKEN']

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )
LOGGER = logging.getLogger()

LANG = 'es'

def start(update, context):
  LOGGER.info(f"User: {update.effective_user['username']}, Chat status: started")
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(words.GREETING[LANG])
    
def helpPrint(update, context):
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(
    parse_mode = 'HTML',
    text = words.HELP[LANG]
    )



#Start Bot
if __name__ == "__main__":
  LOGGER.info("Started!")
  print('Now CLOCKWORK FOX is running!\n')
  
  updater = Updater(token=TOKEN, use_context=True)

  dp = updater.dispatcher
  
  dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcoming.welcoming))
  dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, farewell.farewell))

  dp.add_handler(ConversationHandler(
      entry_points=[
        #COMMANDS
        CommandHandler('start', start),
        CommandHandler('help', helpPrint),
        CommandHandler('new_sfriend', secretFriend.secretFriendStart),
        CommandHandler('finish_sfriend', secretFriend.secretFriendEnd),
        CommandHandler('cancel_sfriend', secretFriend.cancel_sfriend),
        CommandHandler('new_raffle', raffle.startRaffle),
        CommandHandler('finish_raffle', raffle.end_raffle),
        CommandHandler('cancel_raffle', raffle.cancel_raffle),
        #CALLBACKS
        CallbackQueryHandler(pattern='im_in', callback=secretFriend.counter),
        CallbackQueryHandler(pattern='raffle_join', callback=raffle.raffle_join)
      ],

      states={
      },

      fallbacks=[]
  ))


  updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url="https://clockworkfox-bot.herokuapp.com/" + TOKEN)
  updater.idle()

  #updater.start_polling()
  #updater.idle()

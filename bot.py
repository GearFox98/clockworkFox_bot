#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import lib.rhandler as rh
import lib.fshandler as fh
import lib.words as words

from lib import (basicfun,
                 events,
                 raffles)

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


#Server
PORT = int(os.environ.get('PORT', '8443'))

#Token
#TOKEN = os.environ['TOKEN']
TOKEN = "5054914576:AAEu06B-g64rGnErMSIV6JU4wdUWCpIgHBk"

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )
LOGGER = logging.getLogger()

LANG = 'es'

def helpPrint(update, context):
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(
    parse_mode = 'HTML',
    text = words.HELP[LANG]
    )

#Language Options TODO
def changeLang(update, context):
  en = InlineKeyboardButton(
    text = 'English',
    callback_data = 'en'
  )
  
  es = InlineKeyboardButton(
    text = 'Español',
    callback_data = 'es'
  )
  
  update.message.reply_text(
    text = words.LANG[LANG],
    reply_markup = InlineKeyboardMarkup([
      [en],
      [es]
    ])
  )

def eng(update, context):
  query = update.callback_query
  query.answer()
  
  LANG = 'en'
  print(LANG)

def esp(update, context):
  query = update.callback_query
  query.answer()
  
  LANG = 'es'
  print(LANG)



#Start Bot
if __name__ == "__main__":
  LOGGER.info("Started!")
  print('Now CLOCKWORK FOX is running!\n')
  
  updater = Updater(token=TOKEN, use_context=True)

  dp = updater.dispatcher
  
  dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, basicfun.welcoming(updater, context, LOGGER=LOGGER)))

  dp.add_handler(ConversationHandler(
      entry_points=[
        #COMMANDS
        CommandHandler('start', basicfun.start(update, context, LOGGER=LOGGER)),
        CommandHandler('new_sfriend', events.secretFriendStart(LOGGER=LOGGER)),
        CommandHandler('finish_sfriend', events.secretFriendEnd(LOGGER=LOGGER)),
        CommandHandler('help', helpPrint),
        CommandHandler('new_raffle', raffles.raffle(LOGGER=LOGGER)),
        CommandHandler('finish_raffle', raffles.end_raffle(LOGGER=LOGGER)),
        #CommandHandler('language', changeLang), TODO
        CommandHandler('cancel_raffle', raffles.cancel_raffle(LOGGER=LOGGER)),
        CommandHandler('cancel_sfriend', raffles.cancel_sfriend(LOGGER=LOGGER)),
        #CALLBACKS
        CallbackQueryHandler(pattern='im_in', callback=events.counter(LOGGER=LOGGER)),
        CallbackQueryHandler(pattern='raffle_join', callback=raffles.raffle_join(LOGGER=LOGGER)),
        CallbackQueryHandler(pattern='en', callback=eng),
        CallbackQueryHandler(pattern='es', callback=esp)
      ],

      states={
      },

      fallbacks=[]
  ))


  '''updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url="https://clockworkfox-bot.herokuapp.com/" + TOKEN)
  updater.idle()'''

  updater.start_polling()
  updater.idle()

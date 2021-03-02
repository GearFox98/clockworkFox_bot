#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
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
import lib.rhandler as rh
import lib.fshandler as fh
import lib.words as words

PORT = int(os.environ.get('PORT', '8443'))

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
LOGGER = logging.getLogger()

LANG = 'es'
TOKEN = fh.getToken()

#Event variables
#CONTESTANTS = ['None']

CONT = ['None']

def start(update, context):
  LOGGER.info(f"User: {update.effective_user['username']}, Chat status: started")
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(words.GREETING[LANG])
    
def welcoming(update, context):
  bot = context.bot
  chatId = update.message.chat_id
  udp = getattr(update, 'message', None)
  groupName = update.message.chat.title
  
  for user in udp.new_chat_members:
    userName = user.first_name
    is_bot = user.is_bot
  
  if not is_bot:
    context.bot.send_chat_action(chatId, "typing")
    bot.send_message(
      chat_id = chatId,
      parse_mode = 'HTML',
      text = "Hola {} le damos la bienvenida al grupo <b>{}</b>".format(userName, groupName)
    )

def startEvent(update, context):
  id = update.effective_chat.id
  if id < 0:
    userid = update.effective_user.id
    admins = context.bot.get_chat_administrators(id)
    admId = list()
    for adm in admins:
      admId.append(adm.user.id)
    if not admId.__contains__(userid):
      context.bot.send_chat_action(update.effective_chat.id, "typing")
      update.message.reply_text(
        text = "Lo siento, debes ser administrador para crear eventos"
      )
    else:
      if not False: #status:
        txt = context.args
        if len(txt) == 0:
          context.bot.send_chat_action(update.effective_chat.id, "typing")
          context.bot.send_message(
            chat_id = id,
            text = "Lo siento, necesito un mensaje para el evento"
          )
        else:
          if len(CONT) > 0:
            CONT.pop(0)
          text = " ".join(txt)
          context.bot.send_chat_action(update.effective_chat.id, "typing")
          button = InlineKeyboardButton(
            text = words.EVENT[LANG + "_btn"], #TODO
            callback_data = 'im_in'
          )
          context.bot.send_message(
            chat_id = id,
            text = words.EVENT[LANG] + text,
            reply_markup = InlineKeyboardMarkup([
              [button]
            ])
          )
        #fh.setEventStatus(True, id)
      else:
        context.bot.send_message(
          chat_id = id,
          text = "Ya hay un evento activo"
        )
  else:
    update.message.reply_text(text="Lo siento, esta acción solo está permitida en grupos")


def finishEvent(update, context):
  x = rh.doAssignments(CONT)
  if not True: #fh.getEventStatus(update.effective_chat.id):
    context.bot.send_chat_action(update.effective_chat.id, "typing")
    context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = "No hay eventos activos"
    )
  else:
    if x == 'nil':
      context.bot.send_chat_action(update.effective_chat.id, "typing")
      update.message.reply_text(
        text = "No hay suficientes participantes, deben haber al menos 3"
      )
    else:
      CURRENT_GROUP = update.effective_chat.id
      for i in x:
        userid = i[0][0]
        currentuser = i[0][1]
        username = i [1][1]
        try:
          context.bot.send_chat_action(userid, "typing")
          context.bot.send_message(userid,
                                    f'Hola {currentuser} su amigo secreto del evento es: {username}\nRecuerde, debe mantener el secreto hasta el día de entrega'
                                  )
        except Exception as e:
          LOGGER.info(e)
      context.bot.send_chat_action(CURRENT_GROUP, "typing")
      context.bot.send_message(CURRENT_GROUP, 'Todos los concursantes han recibido sus instrucciones, recuerden divertirse\n#CLOCKWORK_EVENT')
      #fh.setEventStatus(False, update.effective_chat.id)

def helpPrint(update, context):
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(words.HELP[LANG])

def counter(update, context):
  query = update.callback_query
  id = query.message.chat.id
  username = query.from_user.username
  userid = query.from_user.id
  userfname = query.from_user.first_name
  
  #CONTESTANTS = fh.readConts(id)
  
  if not username == None:
    x = (userid, "@{}".format(username))
  else:
    x = (userid, userfname)
  if not CONT.__contains__(x):
    try:
      CONT.append(x)
      query.answer('¡Listo!')
      context.bot.send_message(id, f'{userfname} se ha unido al evento!')
    except Exception as ex:
      LOGGER.info(ex)
  else:
    query.answer('Ya estás en el evento')
  #fh.writeConts(CONTESTANTS, id)

#Language Options
def changeLang(update, context):
  en = InlineKeyboardButton(
    text = 'English',
    callback_data = 'en'
  )
  
  es = InlineKeyboardButton(
    text = 'Español',
    callback_data = 'es'
  )
  
  context.bot.send_chat_action(update.effective_chat.id, "typing")
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

if __name__ == "__main__":
  LOGGER.info("Started!")
  print('Now CLOCKWORK FOX is running!\n')
  
  updater = Updater(token=TOKEN, use_context=True)

  dp = updater.dispatcher
  
  dp.add_handler(CommandHandler('start', start))
  
  dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcoming))

  dp.add_handler(ConversationHandler(
      entry_points=[
        #COMMANDS
        CommandHandler('new_event', startEvent),
        CommandHandler('finish_event', finishEvent),
        CommandHandler('help', helpPrint),
        CommandHandler('language', changeLang),
        #CommandHandler('rev', reverse),
        #CALLBACKS
        CallbackQueryHandler(pattern='im_in', callback=counter),
        CallbackQueryHandler(pattern='en', callback=eng),
        CallbackQueryHandler(pattern='es', callback=esp)
      ],

      states={
      },

      fallbacks=[]
  ))

  updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
  updater.bot.set_webhook("https://clockworkfox-bot.herokuapp.com/" + TOKEN)
  updater.idle()

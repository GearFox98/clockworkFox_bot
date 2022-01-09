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

#Server
PORT = int(os.environ.get('PORT', '443'))

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

def helpPrint(update, context):
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(
    parse_mode = 'HTML',
    text = words.HELP[LANG]
    )

#Events
def secretFriendStart(update, context):
  id = update.effective_chat.id
  if id < 0:
    userid = update.effective_user.id
    admins = context.bot.get_chat_administrators(id)
    admId = list()
    for adm in admins:
      admId.append(adm.user.id)
    if not admId.__contains__(userid):
      context.bot.send_chat_action(id, "typing")
      update.message.reply_text(
        text = "Lo siento, debes ser administrador para crear eventos"
      )
    else:
      #Datahandler
      status = fh.getEventStatus(id)
      if not status:
        txt = context.args
        if len(txt) == 0:
          context.bot.send_chat_action(id, "typing")
          context.bot.send_message(
            chat_id = id,
            text = "Lo siento, necesito un mensaje para el evento"
          )
        else:
          text = " ".join(txt)
          context.bot.send_chat_action(id, "typing")
          button = InlineKeyboardButton(
            text = words.EVENT[LANG + "_btn"], #TODO
            callback_data = 'im_in',
          )
          context.bot.send_message(
            chat_id = id,
            text = words.EVENT[LANG] + text,
            parse_mode = 'HTML',
            reply_markup = InlineKeyboardMarkup([
              [button]
            ])
          )
        #Datahandler
        fh.setEventStatus(True, id)
      else:
        context.bot.send_chat_action(id, "typing")
        context.bot.send_message(
          chat_id = id,
          text = "Ya hay un evento activo"
        )
  else:
    update.message.reply_text(text="Lo siento, esta acción solo está permitida en grupos")

def secretFriendEnd(update, context):
  group_id = update.effective_chat.id
  LOGGER.info(f"Effective: {group_id} is finishing event")
  if group_id < 0:
    userid = update.effective_user.id
    LOGGER.info(f"User: {userid} triggered")
    admins = context.bot.get_chat_administrators(group_id)
    admId = list()
    for adm in admins:
      admId.append(adm.user.id)
    if not admId.__contains__(userid):
      LOGGER.warning(f"User {userid} is not an admin")
      context.bot.send_chat_action(group_id, "typing")
      update.message.reply_text(
        text = "Lo siento, debes ser administrador para finalizar eventos"
      )
    else:
      if not fh.getEventStatus(group_id):
        LOGGER.info(f"Chat: {group_id} has not event")
        context.bot.send_message(
          chat_id = group_id,
          text = "No hay eventos activos, para iniciar uno utiliza \\new_event."
        )
      else:
        LOGGER.info(f"Doing assignments")
        CONT = fh.getTempList(group_id)
        x = rh.doAssignments(CONT)
        if x == 'nil':
          LOGGER.warn(f"There's no enough participants")
          update.message.reply_text(
            text = "No hay suficientes participantes, deben haber al menos 3\n<b>Nota</b>: <i>si desea cancelar el evento utilice</i> <b>/cancel_sfriend</b>",
            parse_mode = 'HTML'
          )
          LOGGER.info("Assignments done!")
        else:
          LOGGER.info(f"{group_id} - Delivering")
          for i in x:
            userid = i[0][0]
            currentuser = i[0][1]
            username = i [1][1]
            try:
              context.bot.send_message(userid,
                                        f'Hola {currentuser} su amigo secreto del evento es: {username}\nRecuerde, debe mantener el secreto hasta el día de entrega'
                                      )
            except Exception as e:
              LOGGER.error(f"{group_id} - {e}")
          context.bot.send_message(group_id, 'Todos los concursantes han recibido sus instrucciones, recuerden divertirse\n#CLOCKWORK_EVENT')
          LOGGER.info(f"{group_id} - Delivered")
          fh.setEventStatus(False, group_id)

def counter(update, context):
  query = update.callback_query
  gId = query.message.chat.id
  username = query.from_user.username
  userid = query.from_user.id
  userfname = query.from_user.first_name
  CONT = fh.getTempList(gId)
  
  if not username == None:
    x = (userid, f"@{username}")
  else:
    x = (userid, userfname)
  
  is_there = False
  for temp in CONT:
    if temp[0] == userid:
    
      is_there = True
  
  if not is_there:
    try:
      CONT.append(x)
      query.answer('¡Listo!\nRecuerda iniciarme en privado si no lo has hecho.')
      context.bot.send_message(gId, f"{userfname} se ha unido al evento!")
      fh.setEventList(gId, CONT)
    except Exception as ex:
      LOGGER.info(ex)
  else:
    query.answer('Ya estás en el evento')

#Raffles
def raffle(update, context):
  deleted = update.message.message_id
  gId = update.effective_chat.id
  is_raffle = fh.getIsRaffle(gId)

  if not is_raffle:
    try:
      arg = context.args
      if len(arg) > 1:
        try:
          places = int(arg[-1])
          arg.pop(-1)
          text = " ".join(arg)
        except Exception as _error:
          LOGGER.info("No places were given")
      elif len(arg) == 0:
        context.bot.send_chat_action(gId, "typing")
        update.message.reply_text(text = "Necesito un tema de sorteo")
      else:
        places = 3
        text = arg[0]
      
      button = InlineKeyboardButton(
              text = words.EVENT[LANG + "_btn"],
              callback_data = 'raffle_join',
            )
      
      context.bot.send_chat_action(gId, "typing")
      context.bot.send_message(
        chat_id = gId,
        parse_mode = 'HTML',
        text = text + words.RAFFLE[LANG],
        reply_markup = InlineKeyboardMarkup([
                [button]
              ])
      )
      
      fh.setRaffleMax(gId, update.effective_user.id, places)

      context.bot.delete_message(gId, deleted)
    except Exception as _error:
      LOGGER.error(_error)
  else:
    context.bot.send_message(gId, "Ya hay un sorteo activo")

def raffle_join(update, context):
  query = update.callback_query
  gId = query.message.chat.id
  username = query.from_user.username
  userid = query.from_user.id
  userfname = query.from_user.first_name

  CONT = fh.getRaffleCont(gId)

  if not username == None:
    x = (userid, f"@{username}")
  else:
    x = (userid, userfname)
  
  is_there = False
  for temp in CONT:
    if temp[0] == userid:
      is_there = True
  
  if not is_there:
    try:
      CONT.append(x)
      query.answer('¡Listo!')
      fh.setRaffle(gId, CONT)
      context.bot.send_message(
        chat_id = fh.getAuthor(gId),
        parse_mode = 'HTML',
        text = f"{words.NOTIFICATION[LANG]} {len(CONT)}"
        )
    except Exception as ex:
      LOGGER.error(ex)
  else:
    query.answer('Ya estás en el evento')
  
def end_raffle(update, context):
  gId = update.effective_chat.id
  deleted = update.message.message_id
  
  try:
    context.bot.delete_message(gId, deleted)
  except Exception as _error:
    LOGGER.error(_error)
  finally:
    raffle = fh.getRaffle(gId)
    LOGGER.debug(f"Cont: {raffle}")
    winners = rh.raffle(raffle['cont'], raffle['max'])
    LOGGER.debug(f"Winners: {winners}")

    text = "Los ganadores son:\n"

    for x in winners:
      text += f"\n\t· {x[1]}"

    context.bot.send_message(
      chat_id = gId,
      parse_mode = 'HTML',
      text = text
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

#Cancellations
def cancel_raffle(update, context):
  try:
    if not fh.cancelRaff(update.effective_chat.id, update.effective_user.id):
      update.message.reply_text(text = "Lo siento, solo el autor del sorteo puede cancelarlo")
    else:
      update.message.reply_text(text = "Sorteo cancelado")
  except Exception as _error:
    LOGGER.error(_error)

def cancel_sfriend(update, context):
  gId = update.effective_chat.id
  try:
    LOGGER.info(f"Id de chat: {gId}")
    if gId < 0:
      userid = update.effective_user.id
      admins = context.bot.get_chat_administrators(gId)
      admId = list()
      for adm in admins:
        admId.append(adm.user.id)
      if not admId.__contains__(userid):
        context.bot.send_chat_action(gId, "typing")
        update.message.reply_text(
          text = "Lo siento, debes ser administrador para cancelar eventos"
        )
      else:
        context.bot.send_chat_action(gId, "typing")
        update.message.reply_text(
          text = "Evento cancelado"
        )
        fh.cancelEv(gId)
  except Exception as error:
    context.bot.send_message(gId, str(error))



#Start Bot
if __name__ == "__main__":
  LOGGER.info("Started!")
  print('Now CLOCKWORK FOX is running!\n')
  
  updater = Updater(token=TOKEN, use_context=True)

  dp = updater.dispatcher
  
  dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcoming))

  dp.add_handler(ConversationHandler(
      entry_points=[
        #COMMANDS
        CommandHandler('start', start),
        CommandHandler('new_sfriend', secretFriendStart),
        CommandHandler('finish_sfriend', secretFriendEnd),
        CommandHandler('help', helpPrint),
        CommandHandler('new_raffle', raffle),
        CommandHandler('finish_raffle', end_raffle),
        #CommandHandler('language', changeLang), TODO
        CommandHandler('cancel_raffle', cancel_raffle),
        CommandHandler('cancel_sfriend', cancel_sfriend),
        #CALLBACKS
        CallbackQueryHandler(pattern='im_in', callback=counter),
        CallbackQueryHandler(pattern='raffle_join', callback=raffle_join),
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

  '''updater.start_polling()
  updater.idle()'''

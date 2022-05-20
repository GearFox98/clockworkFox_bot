import logging
import fshandler as fh
import rhandler as rh
import words
from telegram import (InlineKeyboardMarkup,
                      InlineKeyboardButton)

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )
LOGGER = logging.getLogger()

#START
def secretFriendStart(update, context):
  #Don't touch for not TODO
  LANG = 'es'

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

#END
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

#CANCELATOR
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

#COUNTER UTILITY
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
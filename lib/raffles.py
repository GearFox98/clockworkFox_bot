from . import fshandler as fh
from . import rhandler as rh
from . import words

#Raffles
def raffle(update, context, LOGGER):
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

def raffle_join(update, context, LOGGER):
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
  
def end_raffle(update, context, LOGGER):
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

#Cancellations
def cancel_raffle(update, context, LOGGER):
  try:
    if not fh.cancelRaff(update.effective_chat.id, update.effective_user.id):
      update.message.reply_text(text = "Lo siento, solo el autor del sorteo puede cancelarlo")
    else:
      update.message.reply_text(text = "Sorteo cancelado")
  except Exception as _error:
    LOGGER.error(_error)
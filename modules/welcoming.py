import logging
from datetime import datetime
from telegram import chat
from telegram.ext import (Updater,
                        MessageHandler,
                        ConversationHandler)

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )
LOGGER = logging.getLogger()

def welcoming(update, context):
  bot = context.bot
  chat_id = update.message.chat_id
  udp = getattr(update, 'message', None)
  group_name = update.message.chat.title
  
  for user in udp.new_chat_members:
    user_name = user.first_name
    user_alias = user.user_name
    is_bot = user.is_bot
  
  if not is_bot:
    context.bot.send_chat_action(chat_id, "typing")
    bot.send_message(
      chat_id = chat_id,
      parse_mode = 'HTML',
      text = f"Hola {user_name} le damos la bienvenida al grupo <b>{group_name}</b>"
    )

    #Notifying admins
    admins = context.bot.get_chat_administrators(chat_id)
    today = datetime.strftime(datetime.today(), "%d %b %Y - %-I:%M %p")
    inform = f"<b>Nuevo usuario</b>: {user_name}({user_alias})\n<b>Grupo</b>: {group_name}\nHa entrado: <i>{today}</i>"

    for admin in admins:
        try:
            bot.send_message(
                chat_id = admin,
                parse_mode = 'HTML',
                text = inform
            )
        except:
            LOGGER.error(f"Admin {admin} is has not activated Clockwork")
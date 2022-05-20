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

def farewell(update, context):
  bot = context.bot
  chat_id = update.message.chat_id
  udp = getattr(update, 'message', None)
  group_name = update.message.chat.title

  
  user = udp.left_chat_member
  user_name = user.first_name
  user_alias = user.username
  is_bot = user.is_bot
  
  if not is_bot:
    context.bot.send_chat_action(chat_id, "typing")
    bot.send_message(
      chat_id = chat_id,
      parse_mode = 'HTML',
      text = f"{user_name} ya no pertenece a <b>{group_name}</b>"
    )

    #Notifying admins
    admins = context.bot.get_chat_administrators(chat_id)
    today = datetime.strftime(datetime.today(), "%d %b %Y - %-I:%M %p")
    inform = f"<b>Usuario removido</b>: {user_name}(@{user_alias})\n<b>Grupo</b>: {group_name}\nHa sido retirado: <i>{today}</i>"

    for admin in admins:
        try:
            bot.send_message(
                chat_id = admin.user.id,
                parse_mode = 'HTML',
                text = inform
            )
        except Exception as e:
            LOGGER.error(f"Admin {admin} is has not activated Clockwork\n{e}")
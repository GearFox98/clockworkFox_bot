import logging
import cogs.admin as adf
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )

LOGGER = logging.getLogger()

# ADMIN NOTIFY
async def notify(bot, inform, admins):
    for admin in admins:
        try:
            await bot.send_message(
                chat_id = admin.user.id,
                parse_mode = 'HTML',
                text = inform
            )
            LOGGER.info(inform)
        except Exception as e:
            LOGGER.error(f"Admin {admin} is has not activated Clockwork\n{e}")

# USER JOINS
async def welcoming(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    chat_id = update.message.chat_id
    udp = getattr(update, 'message', None)
    group_name = update.message.chat.title
  
    for user in udp.new_chat_members:
        user_name = user.first_name
        user_alias = user.username
        is_bot = user.is_bot
  
    if not is_bot:
        await context.bot.send_chat_action(chat_id, "typing")
        await bot.send_message(
            chat_id = chat_id,
            parse_mode = 'HTML',
            text = f"Hola {user_name} le damos la bienvenida al grupo <b>{group_name}</b>"
        )

    #Notifying admins
    admins = await context.bot.get_chat_administrators(chat_id)
    today = datetime.strftime(datetime.today(), "%d %b %Y - %-I:%M %p")
    inform = f"Nuevo usuario: {user_name}(@{user_alias})\nGrupo: {group_name}\nHa entrado: {today}"

    await adf.uncompat(update, context)
    await notify(bot, inform, admins)


# USER LEAVE
async def farewell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        chat_id = update.message.chat_id
        udp = getattr(update, 'message', None)
        group_name = update.message.chat.title

    
        user = udp.left_chat_member
        user_name = user.first_name
        user_alias = user.username
        is_bot = user.is_bot
    
        if not is_bot:
            await context.bot.send_chat_action(chat_id, "typing")
            await bot.send_message(
                chat_id = chat_id,
                parse_mode = 'HTML',
                text = f"{user_name} ya no pertenece a <b>{group_name}</b>"
            )

        #Notifying admins
        admins = await context.bot.get_chat_administrators(chat_id)
        today = datetime.strftime(datetime.today(), "%d %b %Y - %-I:%M %p")
        inform = f"Usuario removido: {user_name}(@{user_alias})\nGrupo: {group_name}\nHa sido retirado: {today}"

        await adf.uncompat(update, context)
        await notify(bot, inform, admins)
    except Exception as e:
        LOGGER.error(f"{e}")

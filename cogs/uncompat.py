from telegram import Update
from telegram.ext import ContextTypes
from os import getenv

import logging

logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )

LOGGER = logging.getLogger()

async def uncompat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UNCOMPAT_I = getenv("UNCOMPAT_I").split(",")
    UNCOMPAT_U = getenv("UNCOMPAT_U").split(",")
    GUARDIAN = getenv("GUARDIAN")
    bot = context.bot

    #Chat details
    ID = update.effective_chat.id
    GN = update.message.chat.title
    adms = await context.bot.get_chat_administrators(ID)
  
    if ID < 0:
        AI = [adm_id.user.id for adm_id in adms]
        AU = [adm_id.user.username for adm_id in adms]
        AF = [adm_id.user.first_name for adm_id in adms]

        uncompat_v = False

        for i in range(len(UNCOMPAT_I)):
            uncompat_v = int(UNCOMPAT_I[i]) in AI or UNCOMPAT_U[i] in AU

        if uncompat_v:
            try:
                inform = f"Clockwork has left <b>{GN}</b>"
                await bot.send_message(
                    chat_id = GUARDIAN,
                    parse_mode = 'HTML',
                    text = inform
                )
                LOGGER.info(inform)
            except Exception as _e:
                LOGGER.error(f"Clockwork crashed at {GN}\n{AF}")
            finally:
                await bot.leave_chat(ID)

import logging
from cogs.exceptions import Exceptions, RustyCog
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
  )

LOGGER = logging.getLogger()

# Check if bot is admin
async def check_self_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    has_permit = None
    
    admins = await update.effective_chat.get_administrators()
    bot_id = context.bot.id

    if bot_id in [admin.user.id for admin in admins]:
        has_permit = True
    else:
        has_permit = False
        await update.effective_chat.send_action("typing")
        await update.effective_chat.send_message(f"Lo siento, necesito permisos de administración para realizar esta acción")

    return has_permit

# Returns a status or a dictionary
async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    issuer = update.message.from_user.id
    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.user.id == issuer:
            if admin.status == ChatMemberStatus.OWNER:
                return "OWNER"
            else:
                if admin.user.id == issuer:
                    dic = admin.to_dict()
                    return dic
    
    return None

# Ban an user
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_admin = await check_self_admin(update, context)
    print(is_admin)

    if not is_admin:
        return
    else:
        try:
            if update.effective_chat.id < 0:
                if update.message.reply_to_message != None:
                    to_ban_user = update.message.reply_to_message.from_user.id
                else:
                    raise RustyCog(Exceptions.EMPTY_USER)

                # Gets if owner or a dictionary with permissions
                admin = await check_permissions(update, context)

                if admin == "OWNER":
                    # Owner case
                    LOGGER.info(f"The owner of {update.effective_chat.full_name} has issued ban!")
                    await update.effective_chat.ban_member(to_ban_user)
                elif admin != None:
                    # Administrator case
                    if admin['can_restrict_members']:
                        LOGGER.info(f"An admin of {update.effective_chat.full_name} has issued ban!")
                        await update.effective_chat.ban_member(to_ban_user)
                    else:
                        raise RustyCog(Exceptions.CANT_BAN)
                else:
                    # Not an administrator case
                    raise RustyCog(Exceptions.NOT_AN_ADMIN)
            else:
                raise RustyCog(Exceptions.NOT_A_GROUP)
        except RustyCog as e:
            LOGGER.error(f"{e.status} - Address to exceptions module for more info...")
            match e.status:
                case Exceptions.CANT_BAN:
                    await update.effective_chat.send_action("typing")
                    await update.effective_chat.send_message(f"Lo siento, no tienes permitida esa acción")
                    return
                case Exceptions.NOT_A_GROUP:
                    await update.effective_chat.send_action("typing")
                    await update.effective_chat.send_message(f"Esta acción solo funciona en grupos")
                    return
                case Exceptions.EMPTY_USER:
                    await update.effective_chat.send_action("typing")
                    await update.effective_chat.send_message(f"Debes responder al mensaje del usuario a expulsar")
                    return
                case Exceptions.NOT_AN_ADMIN:
                    await update.effective_chat.send_action("typing")
                    await update.effective_chat.send_message(f"No tienes permisos de administrador, no puedes realizar esta acción")
                    return
                case _:
                    await update.effective_chat.send_action("typing")
                    await update.effective_chat.send_message("Ha ocurrido un error, asegúrate de que cuento con los <b>permisos</b> suficientes para hacer esto o que estés <b>respondiendo al mensaje del usuario</b> a expulsar",
                                                       parse_mode="HTML")
                    return

async def uncompat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from os import getenv
    
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
            await feedback(bot, GUARDIAN, GN, AF)
            await bot.leave_chat(ID)

async def feedback(bot, guardian, gname, args):
    try:
        inform = f"Clockwork has leaved <b>{gname}</b>"
        await bot.send_message(
            chat_id = guardian,
            parse_mode = 'HTML',
            text = inform
        )
        LOGGER.info(inform)
    except Exception as e:
        LOGGER.error(f"Clockwork crashed at {gname}\n{args}\n{e}")

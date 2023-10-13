import logging
from cogs.exceptions import Exceptions, RustyCog
from cogs.basics import say
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
        await say(update, context, f"Lo siento, necesito permisos de administración para realizar esta acción")

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

# Notify owner about banning
async def notify_owner(update: Update, context: ContextTypes.DEFAULT_TYPE, issuer, chat):
    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        if admin.status == ChatMemberStatus.OWNER:
            owner = admin.user.id
            
            try:
                await say(update, context, f"Sentencia de expulsión ejecutada por {issuer} en el grupo {chat}", owner)
            except Exception as e:
                LOGGER.error(e)
            finally:
                break

# Elevate user to admin
async def elevate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_admin = await check_self_admin(update, context)

    if not is_admin:
        return
    else:
        permissions = await check_permissions(update, context)

        try:
            if permissions == "OWNER" or permissions["can_promote_members"]:
                u_id = update.message.reply_to_message.from_user.id
                uname = update.message.reply_to_message.from_user.username

                print(f"Get Member: {u_id}")

                await update.effective_chat.promote_member(u_id,
                                                            can_change_info=True,
                                                            can_delete_messages=True,
                                                            can_restrict_members=True,
                                                            can_pin_messages=True,
                                                            can_manage_chat=True,
                                                            can_invite_users=True)

                await say(update, context, f"El usuario @{uname} es ahora administrador")
            else:
                raise RustyCog(Exceptions.NOT_AN_ADMIN)
        except RustyCog as e:
            args = e.status
            LOGGER.error(f"Something happened, CODE: {args}")

            if args == Exceptions.NOT_AN_ADMIN:
                await say(update, context, "Lo siento, no tienes permisos para esto")


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
                    LOGGER.info(f"The owner of {update.effective_chat.title} has issued ban!")
                    if update.message.from_user.id == to_ban_user:
                        await update.message.reply_text("No te puedes banear a ti mismo")
                    else:
                        await update.effective_chat.ban_member(to_ban_user)
                elif admin != None:
                    # Administrator case
                    if admin['can_restrict_members']:
                        LOGGER.info(f"An admin of {update.effective_chat.title} has issued ban!")
                        if update.message.from_user.id == to_ban_user:
                            await update.message.reply_text("No te puedes banear a ti mismo")
                        else:
                            await update.effective_chat.ban_member(to_ban_user)
                            await notify_owner(update, context, update.message.from_user.full_name, update.effective_chat.title)
                    else:
                        raise RustyCog(Exceptions.CANT_BAN)
                else:
                    # Not an administrator case
                    raise RustyCog(Exceptions.NOT_AN_ADMIN)
            else:
                raise RustyCog(Exceptions.NOT_A_GROUP)
        except RustyCog as e:
            status = e.status
            LOGGER.error(f"{status} - Address to exceptions module for more info...")
            if status == Exceptions.CANT_BAN:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message(f"Lo siento, no tienes permitida esa acción")
                return
            elif status == Exceptions.NOT_A_GROUP:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message(f"Esta acción solo funciona en grupos")
                return
            elif status == Exceptions.EMPTY_USER:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message(f"Debes responder al mensaje del usuario a expulsar")
                return
            elif status == Exceptions.NOT_AN_ADMIN:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message(f"No tienes permisos de administrador, no puedes realizar esta acción")
                return
            else:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message("Ha ocurrido un error, asegúrate de que cuento con los <b>permisos</b> suficientes para hacer esto o que estés <b>respondiendo al mensaje del usuario</b> a expulsar",
                                                    parse_mode="HTML")
                return

# Debug admins
async def get_admins_permission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await update.effective_chat.get_administrators()

    for admin in admins:
        print(admin)


# Change admin title
# TODO ** Find out how to work with it **
async def change_admin_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_admin = await check_self_admin(update, context)

    if not is_admin:
        return
    else:
        permissions = await check_permissions(update, context)
        try:
            if permissions == "OWNER" or permissions["can_promote_members"]:
                arg_len = len(context.args)
                print(f"LEN: {arg_len}")
                if arg_len < 2:
                    raise RustyCog(Exceptions.NO_ARGUMENT_PROVIDED)
                else:
                    title = context.args
                    target = title[-1]
                    title = title.pop(-1)

                    admins = await update.effective_chat.get_administrators()

                    u_names = [admin.user.username for admin in admins]

                    if target in u_names:
                        index = u_names.index(target)

                        print(index)

                        admin = admins[index]

                        await update.effective_chat.set_administrator_custom_title(admin.user.id, title)
                        await update.effective_chat.send_action("typing")
                        await update.effective_chat.send_message(f"Título de @{target} cambiado por {title}")
                    else:
                        raise RustyCog(Exceptions.NON_EXISTENT_USER)
            else:
                raise RustyCog(Exceptions.NOT_AN_ADMIN)
        except RustyCog as e:
            status = e.status
            LOGGER.error(f"{status}")

            if status == Exceptions.NOT_AN_ADMIN:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message("Solo un administrador con permisos suficientes puede hacer eso")
            elif status == Exceptions.NON_EXISTENT_USER:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message("No he recibido argumentos suficientes, asegúrate de escribir un título y un nombre de usuario correcto.")
            else:
                await update.effective_chat.send_action("typing")
                await update.effective_chat.send_message("Ha ocurrido un error, asegúrate de que cuento con los <b>permisos</b> suficientes para hacer esto",
                                                         parse_mode="HTML")
                return
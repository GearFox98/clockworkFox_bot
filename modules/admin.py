import re
from telegram import (
                        ChatMemberAdministrator,
                        ChatMember,
                        chat
                     )

def reply(update, context, chat_id, message):
    context.bot.send_chat_action(chat_id, "typing")
    update.message.reply_text(
        parse_mode = 'HTML',
        text = message
        )

def promote(update, context):
    pass

def change_custom_title(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if chat_id < 0:
        #Get admin id list
        admins = [adm_id.user.id for adm_id in context.bot.get_chat_administrators(chat_id)]
        if user_id in admins:
            if len(context.args) < 2:
                reply(update, context, chat_id, "Necesito <b>1</b> usuario y un título entre <b>1 y 16</b> caracteres")
            else:
                #Check admin
                admin = context.args[0]
                admins = [adm_id.user.username for adm_id in context.bot.get_chat_administrators(chat_id)]

                if admin not in admins:
                    reply(update, context, chat_id, f"Usuario: <i>{admin}</i> no es administrador")
                else:
                    index = admins.index(admin)
                    admins = [adm_id.user.id for adm_id in context.bot.get_chat_administrators(chat_id)]

                    admin = admins[index]
                    title = context.args[1:]
                    title = " ".join(title)

                    print(title)
                    print(f"Chat id: {chat_id}")

                    if len(title) < 1 and len(title) > 16:
                        reply(update, context, chat_id, "El título no se encuentra entre el tango de <b>1 y 16</b> letras")
                    else:
                        try:
                            context.bot.set_chat_administrator_custom_title(chat_id, admin, title)
                        except:
                            reply(update, context, chat_id, "Lo siento, este método es solo para super grupos")
        else:
            reply(update, context, chat_id, "Lo siento, esta operación solo puede ser realizada por un <b>administrador</b>")
    else:
        reply(update, context, chat_id, "Solo puedo hacer esto en un grupo")
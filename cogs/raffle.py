import logging
import cogs.databases as db
import cogs.raffler as raffler
import cogs.words as words

from telegram import (Update,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton)

from telegram.ext import ContextTypes

#LOGGER
logging.basicConfig(
  level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)

LOGGER = logging.getLogger()

LANG ='es'

#Raffles
async def startRaffle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deleted = update.message.message_id
    gId = update.effective_chat.id
    is_raffle = db.getIsRaffle(gId)

    if not is_raffle:
        try:
            arg = context.args
            text = ""
            print(arg)
            if len(arg) == 0:
                await context.bot.send_chat_action(gId, "typing")
                await update.message.reply_text(text = "Necesito un tema de sorteo")
                return
            elif len(arg) > 1:
                try:
                    places = int(arg[-1])
                    arg.pop(-1)
                    text = " ".join(arg)
                except Exception as _e:
                    places = 3
                    text = arg[0]
                    LOGGER.info("No places were given, setting places to 3")
      
            button = InlineKeyboardButton(
                text = words.EVENT[LANG + "_btn"],
                callback_data = 'raffle_join',
            )
      
            await context.bot.send_chat_action(gId, "typing")
            await context.bot.send_message(
                chat_id = gId,
                parse_mode = 'HTML',
                text = text + words.RAFFLE[LANG],
                reply_markup = InlineKeyboardMarkup([
                    [button]
                ])
            )
      
            db.setRaffleMax(gId, update.effective_user.id, places)

            await context.bot.delete_message(gId, deleted)
        except Exception as e:
            LOGGER.error(e)
    else:
        await context.bot.send_message(gId, "Ya hay un sorteo activo")

async def raffle_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    gId = query.message.chat.id
    username = query.from_user.username
    userid = query.from_user.id
    userfname = query.from_user.first_name

    CONT = db.getRaffleCont(gId)

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
            await query.answer('¡Listo!')
            db.setRaffle(gId, CONT)
            await context.bot.send_message(
                chat_id = db.getAuthor(gId),
                parse_mode = 'HTML',
                text = f"{words.NOTIFICATION[LANG]} {len(CONT)}"
            )
        except Exception as e:
            LOGGER.error(e)
    else:
        await query.answer('Ya estás en el evento')
  
async def end_raffle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gId = update.effective_chat.id
    deleted = update.message.message_id

    try:
        await context.bot.delete_message(gId, deleted)
    except Exception as e:
        LOGGER.error(e.args[0])
    finally:
        raffle = db.getRaffle(gId)
        LOGGER.debug(f"Cont: {raffle}")
        winners = raffler.raffle(raffle['cont'], raffle['max'])
        LOGGER.debug(f"Winners: {winners}")

    text = "Los ganadores son:\n"

    for x in winners:
      text += f"\n\t· {x[1]}"

    await context.bot.send_chat_action(gId, "typing")
    await context.bot.send_message(
      chat_id = gId,
      parse_mode = 'HTML',
      text = text
    )

#Cancellations
async def cancel_raffle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not db.cancelRaff(update.effective_chat.id, update.effective_user.id):
            await update.effective_chat.send_chat_action("typing")
            await update.message.reply_text(text = "Lo siento, solo el autor del sorteo puede cancelarlo")
        else:
            await update.effective_chat.send_chat_action("typing")
            await update.message.reply_text(text = "Sorteo cancelado")
    except Exception as e:
        LOGGER.error(e)
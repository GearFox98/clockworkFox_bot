import cogs.words as words
import logging

from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOGGER = logging.getLogger()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.info(f"User: {update.effective_user['username']}, Chat status: started")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    await update.message.reply_text(words.GREETING['es'])

async def helpPrint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await context.bot.send_chat_action(update.effective_chat.id, "typing")
  await update.message.reply_text(
    parse_mode = 'HTML',
    text = words.HELP['es']
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(
    text="PONG"
  )

async def say(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, chat_id = None) -> None:
  if chat_id == None:
    await update.effective_chat.send_action("typing")
    await update.effective_chat.send_message(text = message,
                                            parse_mode= "HTML")
  else:
    await context.bot.send_chat_action(chat_id,
                                       action="typing")
    await context.bot.send_message(chat_id,
                                   text=message)
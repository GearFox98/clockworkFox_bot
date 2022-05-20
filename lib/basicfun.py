from . import words

def start(update, context, LOGGER):
  LOGGER.info(f"User: {update.effective_user['username']}, Chat status: started")
  context.bot.send_chat_action(update.effective_chat.id, "typing")
  update.message.reply_text(words.GREETING[LANG])
    
def welcoming(update, context, LOGGER):
  bot = context.bot
  chatId = update.message.chat_id
  udp = getattr(update, 'message', None)
  groupName = update.message.chat.title
  
  for user in udp.new_chat_members:
    userName = user.first_name
    is_bot = user.is_bot
  
  if not is_bot:
    context.bot.send_chat_action(chatId, "typing")
    bot.send_message(
      chat_id = chatId,
      parse_mode = 'HTML',
      text = "Hola {} le damos la bienvenida al grupo <b>{}</b>".format(userName, groupName)
    )
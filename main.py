import os

import logging

#Basic Functions
from cogs.basics import start, ping, helpPrint
from cogs import greet, raffle, admin

from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          filters)

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

LOGGER = logging.getLogger()

# Token
TOKEN = os.getenv("TOKEN")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development") # Development / Production

# Server
PORT = int(os.environ.get('PORT', '8443'))


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    BASIC_HANDLERS = [CommandHandler("ping", ping),
                      CommandHandler("start", start),
                      CommandHandler("help", helpPrint),
                      MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet.welcoming),
                      MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, greet.farewell)]

    EVENT_HANDLERS = [CommandHandler('new_raffle', raffle.startRaffle),
                      CommandHandler('finish_raffle', raffle.end_raffle),
                      CommandHandler('cancel_raffle', raffle.cancel_raffle)]

    ADMIN_HANDLERS = [CommandHandler('ban', admin.ban_user),
                      CommandHandler('promote', admin.elevate)]

    CALLBACK_HANDLERS = [CallbackQueryHandler(pattern='raffle_join', callback=raffle.raffle_join)]

    DEV_HANDLERS = [CommandHandler('get_admin', admin.get_admins_permission)]

    # Attaching handlers
    app.add_handlers(BASIC_HANDLERS)
    app.add_handlers(EVENT_HANDLERS)
    app.add_handlers(ADMIN_HANDLERS)
    app.add_handlers(CALLBACK_HANDLERS)
    app.add_handlers(DEV_HANDLERS)

    if ENVIRONMENT == "development":
        # Development
        app.run_polling()
    else:
        # Production
        app.run_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url=f"https://clockworkfoxbot.onrender.com/{TOKEN}")


main()
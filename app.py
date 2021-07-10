from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot import NicoleBot
from config import *

import re

def app():
    """Start the bot."""
    nicole = NicoleBot()
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", nicole.start, filters = (Filters.command | Filters.regex(r'^/start@[\w.]+$'))))
    dp.add_handler(CommandHandler("menu", nicole.start, filters = (Filters.command | Filters.regex(r'^/menu@[\w.]+$'))))
    dp.add_handler(CommandHandler("dev", nicole.dev, filters = (Filters.command | Filters.regex(r'^/dev@[\w.]+$'))))

    dp.add_handler(CommandHandler("slap", nicole.slap, filters = (Filters.command | Filters.regex(r'^/slap@[\w.]+$'))))
    dp.add_handler(CommandHandler("roast", nicole.roast, filters = (Filters.command | Filters.regex(r'^/roast@[\w.]+$'))))

    dp.add_handler(CallbackQueryHandler(nicole.menu_actions, pattern=re.compile(r'^main'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.img_actions, pattern=re.compile(r'^img'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.txt_actions, pattern=re.compile(r'^txt'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.exe_actions, pattern=re.compile(r'^exe'), run_async=True))

    dp.add_handler(MessageHandler(Filters.text, nicole.respond))

    dp.add_error_handler(nicole.error)

    # updater.start_polling()
    updater.start_webhook(listen='0.0.0.0', port=int(PORT), webhook_url=URL)

    updater.idle()

if __name__ == '__main__':
    app()
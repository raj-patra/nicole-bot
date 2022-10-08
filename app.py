import os
import re

from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from bot import NicoleBot
from handler import CHandler
from helpers.constants import meme_handler

PORT = os.environ.get('PORT', 3000)
AUTH = os.environ.get('NICOLE_BOT_TOKEN')
# HOOK = os.environ.get('WEBHOOK')
HOOK = "https://1353-2405-201-c009-4005-21ec-d6c2-531a-f16e.ngrok.io"

def app():
    bot = NicoleBot()
    cmd = CHandler()
    updater = Updater(AUTH, use_context=True)
    
    start = ["start", "menu"]
    memes = list(meme_handler.keys())

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(start, bot.start, filters = (Filters.command)))
    dp.add_handler(CommandHandler("help", cmd.help, filters = (Filters.command)))
    dp.add_handler(CommandHandler("dev", cmd.dev, filters = (Filters.command)))
    dp.add_handler(CommandHandler("roast", cmd.roast, filters = (Filters.command)))
    dp.add_handler(CommandHandler(memes, cmd.meme, filters = (Filters.command)))

    dp.add_handler(CallbackQueryHandler(bot.menu_actions, pattern=re.compile(r'^main'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.quiz_actions, pattern=re.compile(r'^quiz'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.img_actions, pattern=re.compile(r'^img'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.txt_actions, pattern=re.compile(r'^txt'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.fun_actions, pattern=re.compile(r'^fun'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.rdm_actions, pattern=re.compile(r'^rdm'), run_async=True))
    dp.add_handler(CallbackQueryHandler(bot.exe_actions, pattern=re.compile(r'^exe'), run_async=True))
    dp.add_handler(CallbackQueryHandler(cmd.help_actions, pattern=re.compile(r'^help'), run_async=True))

    dp.add_handler(MessageHandler(Filters.text, bot.respond))
    dp.add_error_handler(bot.error)

    updater.start_webhook(listen='0.0.0.0', port=PORT, webhook_url=HOOK)
    updater.idle()

if __name__ == '__main__':
    app()

import os
import re

from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from bot import NicoleBot
from handler import CHandler
from helpers.constants import meme_handler

PORT = os.environ.get('PORT', 3000)
TOKEN = os.environ.get('NICOLE_BOT_TOKEN')
HOOK = os.environ.get('WEBHOOK')
HOOK = "https://fc01-2405-201-c009-4087-794c-2471-445c-4203.ngrok.io"

def app() -> None:
    bot = NicoleBot()
    cmd = CHandler()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler(["start", "menu"], bot.start, filters = (filters.COMMAND)))
    application.add_handler(CommandHandler("help", cmd.help, filters = (filters.COMMAND)))
    application.add_handler(CommandHandler("dev", cmd.dev, filters = (filters.COMMAND)))
    application.add_handler(CommandHandler("roast", cmd.roast, filters = (filters.COMMAND)))
    application.add_handler(CommandHandler(list(meme_handler.keys()), cmd.meme, filters = (filters.COMMAND)))

    application.add_handler(CallbackQueryHandler(bot.menu_actions, pattern=re.compile(r'^main')))
    application.add_handler(CallbackQueryHandler(bot.quiz_actions, pattern=re.compile(r'^quiz')))
    application.add_handler(CallbackQueryHandler(bot.image_actions, pattern=re.compile(r'^image')))
    application.add_handler(CallbackQueryHandler(bot.quote_actions, pattern=re.compile(r'^quote')))
    application.add_handler(CallbackQueryHandler(bot.joke_actions, pattern=re.compile(r'^joke')))
    application.add_handler(CallbackQueryHandler(bot.trivia_actions, pattern=re.compile(r'^trivia')))
    application.add_handler(CallbackQueryHandler(bot.service_actions, pattern=re.compile(r'^service')))
    application.add_handler(CallbackQueryHandler(bot.misc_actions, pattern=re.compile(r'^misc')))
    application.add_handler(CallbackQueryHandler(cmd.help_actions, pattern=re.compile(r'^help')))

    application.add_handler(MessageHandler(filters.TEXT, bot.respond))
    application.add_error_handler(bot.error)

    application.run_webhook(listen='0.0.0.0', port=PORT, webhook_url=HOOK)

if __name__ == '__main__':
    app()

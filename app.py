from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot import NicoleBot
from handler import CMDHandler

import re, os

PORT = int(os.environ.get('PORT', 3000))
URL = 'https://nicole-bot.herokuapp.com/'
TOKEN = str(os.environ['BOT_TOKEN'])

def app():
    """Start the bot."""
    nicole = NicoleBot()
    cmd = CMDHandler()
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(["start", "menu"], nicole.start, filters = (Filters.command)))

    dp.add_handler(CommandHandler("help", cmd.help, filters = (Filters.command)))
    dp.add_handler(CommandHandler("dev", cmd.dev, filters = (Filters.command)))
    
    dp.add_handler(CommandHandler("roast", cmd.roast, filters = (Filters.command)))
    dp.add_handler(CommandHandler(["slap", "shit", "bruh", "haha", "doge", "weak"], cmd.meme, filters = (Filters.command)))

    dp.add_handler(CallbackQueryHandler(nicole.menu_actions, pattern=re.compile(r'^main'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.img_actions, pattern=re.compile(r'^img'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.txt_actions, pattern=re.compile(r'^txt'), run_async=True))
    dp.add_handler(CallbackQueryHandler(nicole.exe_actions, pattern=re.compile(r'^exe'), run_async=True))
    dp.add_handler(CallbackQueryHandler(cmd.help_actions, pattern=re.compile(r'^help'), run_async=True))

    dp.add_handler(MessageHandler(Filters.text, nicole.respond))
    dp.add_error_handler(nicole.error)

    updater.start_webhook(listen='0.0.0.0', port=int(PORT), webhook_url=URL)
    updater.idle()

if __name__ == '__main__':
    app()
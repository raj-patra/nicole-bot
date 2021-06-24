from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# from config import *
from bot import NicoleBot

import os

PORT = int(os.environ.get('PORT', 8443))
TOKEN = str(os.environ['BOT_TOKEN'])

def main():
    """Start the bot."""
    nicole = NicoleBot()
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", nicole.start))
    dp.add_handler(CommandHandler("dev", nicole.dev))
    dp.add_handler(CallbackQueryHandler(nicole.menu_actions))
    dp.add_handler(MessageHandler(Filters.text, nicole.respond))

    dp.add_error_handler(nicole.error)

    # updater.start_polling()
    updater.start_webhook(listen='0.0.0.0', port=int(PORT), url_path=TOKEN, webhook_url='https://nicole-bot.herokuapp.com/' + TOKEN)
    # updater.bot.setWebhook('https://nicole-bot.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
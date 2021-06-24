from flask import Flask, request
from config import *
from bot import NicoleBot
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

PORT = int(os.environ.get('PORT', 8443))
# URL = 'https://nicole-bot.herokuapp.com/'

app = Flask(__name__)
nicole = NicoleBot()
updater = Updater(TOKEN, use_context=True)

@app.route('/'+TOKEN, methods=['POST', 'GET'])
def respond():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", nicole.start))
    dp.add_handler(CommandHandler("dev", nicole.dev))
    dp.add_handler(CallbackQueryHandler(nicole.menu_actions))
    dp.add_handler(MessageHandler(Filters.text, nicole.respond))

    dp.add_error_handler(nicole.error)

    return "Response Sent"


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    try:   
        # s = bot.start_webhook(listen='https://6b1c8f97d9e1.ngrok.io', port=8443)
        s = updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://nicole-bot.herokuapp.com/' + TOKEN)
        # s = updater.start_webhook(listen='0.0.0.0', port=int(PORT), webhook_url='https://1105154ec255.ngrok.io')
        # s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        return "webhook setup ok"
    except Exception as e:
        return "webhook setup failed "+str(e)



if __name__ == '__main__':
    app.run(threaded=True, port=PORT, debug=True)
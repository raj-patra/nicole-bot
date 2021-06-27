from flask import Flask, request
from bot import NicoleBot
import os, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

PORT = int(os.environ.get('PORT', 3000))
TOKEN = str(os.environ['BOT_TOKEN'])
URL = 'https://e9352f78c058.ngrok.io'

app = Flask(__name__)
nicole = NicoleBot()
updater = Updater(TOKEN, use_context=True)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route('/', methods=['POST', 'GET'])
def respond():

    print("Hello World")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", nicole.start))
    dp.add_handler(CommandHandler("dev", nicole.dev))
    dp.add_handler(CallbackQueryHandler(nicole.menu_actions))
    dp.add_handler(MessageHandler(Filters.text, nicole.respond))

    dp.add_error_handler(nicole.error)
    updater.idle()
    return "Response Sent"


@app.route('/set', methods=['GET', 'POST'])
def set_webhook():
    try:   
        #updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://nicole-bot.herokuapp.com/' + TOKEN)
        updater.start_webhook(listen='0.0.0.0', port=int(PORT), webhook_url=URL)
        #bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        
        return "webhook setup ok"
    except Exception as e:
        return "webhook setup failed "+str(e)



if __name__ == '__main__':
    app.run(threaded=False, port=PORT, debug=True)
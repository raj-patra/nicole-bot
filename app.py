from flask import Flask, request
import telegram, logging
from config import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

URL = 'https://nicole-bot.herokuapp.com/'

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Hi! I am Nicole, a conversational chatbot. GLHF")

def help(update, context):
    update.message.reply_text("Made with Py3 and AIML. For any queries contact https://t.me/a_ignorant_mortal")

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():

    # Create the Updater and pass it to your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Adding commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    try:
        s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        return "webhook setup ok"
    except Exception as e:
        return "webhook setup failed "+str(e)


@app.route('/')
def index():
    return 'Hey'


if __name__ == '__main__':
    app.run(threaded=True)
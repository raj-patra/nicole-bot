import logging, os, aiml
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = str(os.environ['BOT_TOKEN'])

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialise AIML Kernel
kernel = aiml.Kernel()
kernel.setBotPredicate("name", "Nicole")

# Load/Learn Brain file
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
    kernel.saveBrain("bot_brain.brn")

def start(update, context):
    update.message.reply_text("Hi! I am Nicole, a conversational chatbot. GLHF")

def help(update, context):
    update.message.reply_text("Made with Py3 and AIML. For any queries contact https://t.me/a_ignorant_mortal")

def respond(update, context):
    update.message.reply_text(kernel.respond(update.message.text))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# PORT = int(os.environ.get('PORT', 8443))

def main():
    """Start the bot."""

    # Create the Updater and pass it to your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Adding commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, respond))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen='0.0.0.0', port=int(PORT), url_path=TOKEN)
    # updater.bot.setWebhook('https://nicole-bot.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
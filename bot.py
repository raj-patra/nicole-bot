import logging, os, aiml, requests, pickle, random, string
import telegram as tg

from PIL import Image
from bs4 import BeautifulSoup


class NicoleBot:
    def __init__(self):
        # Initialise AIML Kernel
        self.kernel = aiml.Kernel()
        self.kernel.setBotPredicate("name", "Nicole")

        # Load/Learn Brain file
        if os.path.isfile("bot_brain.brn"):
            self.kernel.bootstrap(brainFile="bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
            self.kernel.saveBrain("bot_brain.brn")

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.iig = pickle.load(open("iig.pickle", "rb"))

        self.main_menu =[
                            [tg.InlineKeyboardButton('Image based APIs', callback_data="image")],
                            [tg.InlineKeyboardButton('Text based APIs', callback_data="text")],
                            [tg.InlineKeyboardButton('Utilities', callback_data="tools")],
                        ]
        self.image_menu=[
                            [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='person')],
                            [tg.InlineKeyboardButton('Cute Doggo 🐶', callback_data='doggo'), tg.InlineKeyboardButton('Little Kitty 🐱', callback_data='kitty')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='back')]
                        ]
        self.text_menu =[
                            [tg.InlineKeyboardButton('Irish Insults 🇮🇪', callback_data='iig'), tg.InlineKeyboardButton('Rare Insults 💥', callback_data='rar')], 
                            [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='rdm')],
                            [tg.InlineKeyboardButton('Age Predictor', callback_data='age')],
                            [tg.InlineKeyboardButton('\u25C0 Back', callback_data='back')]
                        ]
        self.tool_menu =[
                            [tg.InlineKeyboardButton('10 Digit Password Generator', callback_data='pwd')],
                            [tg.InlineKeyboardButton('\u25C0 Back', callback_data='back')]
                        ]

    def start(self, update, context):
        self.kernel.setPredicate("name", "Chodi")
        print(update)
        reply_markup = tg.InlineKeyboardMarkup(self.main_menu)
        update.message.reply_text("Hi! I am Nicole, a conversational chatbot. \n\nUse the menu for tools or send a text to chat. \nGLHF", reply_markup=reply_markup)

    def update_chat(self, query, context, chat_id, message_id, menu):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        reply_markup = tg.InlineKeyboardMarkup(menu)
        query.message.reply_text(text='Choose your Poison :', reply_markup=reply_markup)

    def menu_actions(self, update, context):
        query=update.callback_query

        if query.data == 'image':
            reply_markup = tg.InlineKeyboardMarkup(self.image_menu)
            query.message.edit_text(text='Choose your Poison :', reply_markup=reply_markup)

        elif query.data == 'text':
            reply_markup = tg.InlineKeyboardMarkup(self.text_menu)
            query.message.edit_text(text='Choose your Poison :', reply_markup=reply_markup)

        elif query.data == 'tools':
            reply_markup = tg.InlineKeyboardMarkup(self.tool_menu)
            query.message.edit_text(text='What can I help you with? :', reply_markup=reply_markup)

        elif query.data == 'back':
            reply_markup = tg.InlineKeyboardMarkup(self.main_menu)
            query.message.edit_text(text='What can I help you with? :', reply_markup=reply_markup)
        
        # Functionalities from Image Menu
        if query.data == 'doggo':
            doggo = requests.get("https://dog.ceo/api/breeds/image/random").json()['message']
            caption = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1").json()[0]['fact']

            context.bot.send_photo(chat_id=query.message.chat.id, photo=doggo, caption="Dog Fact - "+caption)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.image_menu)

        if query.data == 'kitty':
            kitty = requests.get("https://thatcopy.pw/catapi/rest/").json()['url']
            caption = requests.get("https://cat-fact.herokuapp.com/facts/random").json()['text']

            context.bot.send_photo(photo=kitty, caption="Cat Fact - "+caption, chat_id=query.message.chat.id)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.image_menu)

        if query.data == 'person':
            msg = "This person does not exist. \nIt was imagined by a GAN (Generative Adversarial Network) \n\nReference - https://thispersondoesnotexist.com"
            url = 'https://thispersondoesnotexist.com/image'

            im = Image.open(requests.get(url, stream=True).raw)
            im.save('static/person.png', 'PNG')

            context.bot.send_photo(photo=open('static/person.png', 'rb'), caption=msg, chat_id=query.message.chat.id)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.image_menu)

        # Functionalities from Text Menu
        if query.data == 'iig':
            insult = (' ').join([random.choice(self.iig['subject']), random.choice(self.iig['adjective']), random.choice(self.iig['noun']), random.choice(self.iig['predicate'])])
            msg = "An Irish man walked into the bar and said \n\n"+insult
            
            context.bot.send_message(chat_id=query.message.chat.id, text=msg)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.text_menu)
        
        if query.data == 'rar':
            insult = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()['insult']
            context.bot.send_message(chat_id=query.message.chat.id, text=insult)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.text_menu)

        if query.data == 'rdm':
            rdm = requests.get('https://www.boredbutton.com/random')
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]

            msg = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n{}\n\nFor best results, use a PC.".format(site)
            context.bot.send_message(chat_id=query.message.chat.id, text=msg)
            
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.text_menu)

        if query.data == 'age':
            name = query.message.chat.first_name
            age = str(requests.get("https://api.agify.io/?name={}".format(name)).json()['age'])
            msg = "Based on my knowledge, I think a person with the name {} would be {} years old \nI might be wrong tho :') \n\nReference: https://agify.io/ \nAgify predicts the age of a person given their name based on analytics, ad segmenting, demographic statistics etc.".format(name, age)

            context.bot.send_message(chat_id=query.message.chat.id, text=msg)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.text_menu)
        
        # Functionalities from Tools Menu
        if query.data == 'pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

            context.bot.send_message(chat_id=query.message.chat.id, text="Here's your password")
            context.bot.send_message(chat_id=query.message.chat.id, text=pwd)
            self.update_chat(query, context, query.message.chat.id, query.message.message_id, self.tool_menu)

        
    def dev(self, update, context):
        update.message.reply_text("Made with Py3 and AIML. \nFor any queries contact https://t.me/a_ignorant_mortal \n\nMore about the dev: https://linktr.ee/ign_mortal")

    def respond(self, update, context):
        update.message.reply_text(self.kernel.respond(update.message.text))

    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)


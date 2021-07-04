import logging, os, aiml, requests, random, string, re, time
import telegram as tg

from PIL import Image
from bs4 import BeautifulSoup
from config import *

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

        self.main_menu =[
                            [tg.InlineKeyboardButton('Image APIs 🌆', callback_data="image"), tg.InlineKeyboardButton('Text APIs 📝', callback_data="text")],
                            [tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="tools")],
                            [tg.InlineKeyboardButton('Cancel Op ❌', callback_data='cancel')]
                        ]
        self.image_menu=[
                            [tg.InlineKeyboardButton('Summon a Meme 🤙', callback_data='meme')],
                            [tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='namo')],
                            [tg.InlineKeyboardButton('Cute Doggo 🐶', callback_data='doggo'), tg.InlineKeyboardButton('Little Kitty 🐱', callback_data='kitty')],
                            [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='human')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='cancel')]
                        ]
        self.text_menu =[
                            [tg.InlineKeyboardButton('Daily Activity 🎬', callback_data='daily')],
                            [tg.InlineKeyboardButton('Quote of the Day 💯', callback_data='quote'), tg.InlineKeyboardButton('Fact of the Day 🤯', callback_data='facts')],
                            [tg.InlineKeyboardButton('Kanye REST 🧭', callback_data='kanye'), tg.InlineKeyboardButton('Donald Grump 🎺', callback_data='trump')], 
                            [tg.InlineKeyboardButton('A Literati\'s Wet Dream 🎶', callback_data='poems')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='cancel')]
                        ]
        self.tool_menu =[
                            [tg.InlineKeyboardButton('Useful Websites </>', callback_data='web')],
                            [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='rdm'), tg.InlineKeyboardButton('Age Predictor 🔞', callback_data='age')],
                            [tg.InlineKeyboardButton('10 Digit Password Generator', callback_data='pwd')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='cancel')]
                        ]

    def start(self, update, context):
        self.kernel.setPredicate("name", "Stranger")
        reply_markup = tg.InlineKeyboardMarkup(self.main_menu)
        intro = """Hi! I am *Nicole*, a conversational chatbot. \n\nUse the /menu for tools or send a text to chat. \nGLHF"""
        menu = "Choose your poison: "
        if "/menu" in update.message.text:
            update.message.reply_text(menu, reply_markup=reply_markup)
        elif "/start"in update.message.text:
            update.message.reply_text(intro, parse_mode="Markdown")

    def update_chat(self, context, chat_id, message_id, menu, text="Choose your Poison :"):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        reply_markup = tg.InlineKeyboardMarkup(menu)
        time.sleep(2)
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def menu_actions(self, update, context):
        query=update.callback_query
        chat_id = query.message.chat.id
        msg_id = query.message.message_id

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
        
        elif query.data == 'cancel':
            context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            context.bot.send_message(chat_id=chat_id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

        # Functionalities from Image Menu
        if query.data == 'doggo':
            doggo = requests.get(DOG_PIC_URL).json()['message']
            # caption = requests.get(DOG_CAP_URL).json()[0]['fact']

            context.bot.send_photo(chat_id=chat_id, photo=doggo, caption="Dog Fact - "+"Random Dog Fact expected here. Error occured")
            self.update_chat(context, chat_id, msg_id, self.image_menu)

        if query.data == 'kitty':
            kitty = requests.get(CAT_PIC_URL).json()['url']
            # caption = requests.get(CAT_CAP_URL).json()['text']

            context.bot.send_photo(photo=kitty, caption="Cat Fact - "+"Random Cat Fact expected here. Error occured", chat_id=chat_id)
            self.update_chat(context, chat_id, msg_id, self.image_menu)

        if query.data == 'human':
            msg = "This person does not exist. \nIt was imagined by a GAN (Generative Adversarial Network) \n\nReference - [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com)"

            im = Image.open(requests.get(RANDOM_HUMAN_URL, stream=True).raw)
            im.save('static/person.png', 'PNG')

            context.bot.send_photo(photo=open('static/person.png', 'rb'), caption=msg, chat_id=chat_id, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.image_menu)

        if query.data == 'meme':
            response = requests.get(MEME_URL).json()
            meme = response["url"]
            caption = """*{}* \n\nPosted in [r/{}](www.reddit.com/r/{}) by [u/{}](www.reddit.com/user/{}) \nLink - {}
            
            """.format(response['title'], response['subreddit'], response['subreddit'], response['author'], response['author'], response['postLink'])

            if response['nsfw'] == True:
                caption += "#nsfw"
            if response['spoiler'] == True:
                caption += "#spolier"

            if meme.split('.')[-1] == 'gif':
                context.bot.sendDocument(chat_id=chat_id, document = meme, caption=caption, parse_mode="Markdown")
            else:
                context.bot.send_photo(chat_id=chat_id, photo=meme, caption=caption, parse_mode="Markdown")

            self.update_chat(context, chat_id, msg_id, self.image_menu)

        if query.data == 'namo':
            response = requests.get(NAMO_URL).json()[0]
            meme = response["url"]
            context.bot.send_photo(chat_id=chat_id, photo=meme, caption="NaMo 🙏🏻", parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.image_menu)

        # Functionalities from Text Menu
        if query.data == 'quote':
            response = requests.get(QUOTE_URL).json()
            msg = "_{}_ \n\n- {}".format(response['content'], response['author'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)

        if query.data == 'kanye':
            response = requests.get(KANYE_URL).json()
            msg = "Kanye REST once said, \n\n_{}_".format(response['quote'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)
            
        if query.data == 'trump':
            response = requests.get(TRUMP_URL).json()
            msg = "Grumpy Donald once said, \n\n_{}_".format(response['message'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)
        
        if query.data == 'daily':
            response = requests.get(DAILY_URL).json()
            msg = "Bored out your mind? \nI can suggest you something to try something out. \n\nActivity - *{}*\nType - *{}*\nParticipants Suggested - *{}*\n\n_Take it as a challenge ;)_".format(response["activity"], response["type"], response["participants"])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)

        if query.data == 'facts':
            response = requests.get(FACTS_URL).json()
            msg = "Did you know, \n\n_{}_".format(response['text'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)
        
        if query.data == 'poems':
            response = random.choice(requests.get(POEMS_URL).json())
            msg = "*{}* \n\n{} \n\nBy *{}*".format(response['title'], response['content'], response['poet']['name'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.text_menu)

        # Functionalities from Tools Menu
        if query.data == 'rdm':
            rdm = requests.get(RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]

            msg = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            
            self.update_chat(context, chat_id, msg_id, self.tool_menu)

        if query.data == 'pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

            context.bot.send_message(chat_id=chat_id, text="Here's your password")
            context.bot.send_message(chat_id=chat_id, text=pwd)
            self.update_chat(context, chat_id, msg_id, self.tool_menu)

        if query.data == 'age':
            name = query.message.chat.first_name
            age = str(requests.get(AGE_URL+"?name={}".format(name)).json()['age'])
            msg = "Based on my knowledge, I think a person with the name {} would be {} years old \nI might be wrong tho :') \n\nReference: [Agify.io](https://agify.io/) \n\n_Agify predicts the age of a person given their name based on analytics, ad segmenting, demographic statistics etc._".format(name, age)

            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            self.update_chat(context, chat_id, msg_id, self.tool_menu)
        
        if query.data == 'web':
            msg = USEFUL_WEBSITE_URL
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown", disable_web_page_preview=True)
            self.update_chat(context, chat_id, msg_id, self.tool_menu)

    def dev(self, update, context):
        info = "Made with Py3 and AIML. \nFor any queries contact, [a_ignorant_mortal](https://t.me/a_ignorant_mortal) \n\nMore about the dev: [Linktree](https://linktr.ee/ign_mortal)"
        update.message.reply_text(info, parse_mode="Markdown")

    def slap(self, update, context):
        chat_id = update.message.chat.id
        mention = update.message.text[5:].strip()
        # user_id = int(str(update).split("'id': ")[-1].split(',')[0])
        user_id = int(re.findall(r'[0-9]+', str(update.message))[-1])

        photo = random.choice(context.bot.getUserProfilePhotos(user_id=user_id)['photos'])
        file_id = photo[0]['file_id']
        file_path = context.bot.getFile(file_id)['file_path']

        slap = Image.open("static/slap.jpg")
        profile = Image.open(requests.get(file_path, stream=True).raw)
        resized_im = profile.resize((round(slap.size[0]*0.22), round(slap.size[1]*0.22)))

        # slap.paste(resized_im, (95,280))
        slap.paste(resized_im, (210, 225))
        slap.save('static/slapped.png', 'PNG')

        if mention == '':
            msg = "You get what you f'in deserve."
        else:
            msg = "{}, You get what you f'in deserve.".format(mention)

        context.bot.send_photo(photo=open('static/slapped.png', 'rb'), caption=msg, chat_id=chat_id)

    def roast(self, update, context):
        mention = update.message.text[6:].strip()
        insult = requests.get(INSULT_URL).json()['insult']
        msg = ", ".join([mention, insult])
        if mention == '':
            context.bot.send_message(chat_id=update.message.chat.id, text=insult)
        else:
            context.bot.send_message(chat_id=update.message.chat.id, text=msg)

    def respond(self, update, context):
        update.message.reply_text(self.kernel.respond(update.message.text))

    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)
        print(update)
        msg = "Hmmm. Something went wrong. This wasn't supposed to happen though. Please try something else while we look into it. ʘ‿ʘ"
        self.update_chat(context, update.callback_query.message.chat.id, update.callback_query.message.message_id, self.main_menu, text=msg)


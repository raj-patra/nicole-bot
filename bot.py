import logging, os, aiml, requests, random, string, re, time
import telegram as tg

from PIL import Image
from bs4 import BeautifulSoup
from config import *

class NicoleBot:
    def __init__(self):
        # Initialise AIML Kernel
        self.kernel = aiml.Kernel()
        self.kernel.verbose(0)
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
                            [tg.InlineKeyboardButton('Image APIs 🌆', callback_data="main_image"), tg.InlineKeyboardButton('Text APIs 📝', callback_data="main_text")],
                            [tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_tools")],
                            [tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ]
        self.image_menu=[
                            [tg.InlineKeyboardButton('Reddit Guild 🤙', callback_data='img_meme'), tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='img_namo')],
                            [tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='img_hero')],
                            [tg.InlineKeyboardButton('Cute Doggo 🐶', callback_data='img_doggo'), tg.InlineKeyboardButton('Little Kitty 🐱', callback_data='img_kitty')],
                            [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='img_human')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ]
        self.text_menu =[
                            [tg.InlineKeyboardButton('Quote of the Day 💯', callback_data='txt_quote'), tg.InlineKeyboardButton('Fact of the Day 🤯', callback_data='txt_facts')],
                            [tg.InlineKeyboardButton('A Literati\'s Wet Dream 🎶', callback_data='txt_poems')],
                            [tg.InlineKeyboardButton('Kanye REST 🧭', callback_data='txt_kanye'), tg.InlineKeyboardButton('Donald Grump 🎺', callback_data='txt_trump')], 
                            [tg.InlineKeyboardButton('Daily Activity 🎬', callback_data='txt_daily')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ]
        self.tool_menu =[
                            [tg.InlineKeyboardButton('Useful Websites </>', callback_data='exe_web')],
                            [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='exe_rdm'), tg.InlineKeyboardButton('Age Predictor 🔞', callback_data='exe_age')],
                            [tg.InlineKeyboardButton('10 Digit Password Generator', callback_data='exe_pwd')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ]

    def __str__(self):
        return "Nicole, is a conversational chatbot made to serve as a telegram client side bot."

    def start(self, update, context):
        self.kernel.setPredicate("name", "Stranger")
        reply_markup = tg.InlineKeyboardMarkup(self.main_menu)
        intro = """Hi! I am *Nicole*, a conversational chatbot. \n\nUse the /menu for tools or send a text to chat. \nGLHF"""
        menu = "Choose your poison: "
        if "/menu" in update.message.text:
            update.message.reply_text(menu, reply_markup=reply_markup)
        elif "/start"in update.message.text:
            update.message.reply_text(intro, parse_mode="Markdown")

    def update_chat(self, context, chat_id, menu, text="Choose your Poison :"):
        reply_markup = tg.InlineKeyboardMarkup(menu)
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def menu_actions(self, update, context):
        query = update.callback_query
        chat_id = query.message.chat.id
        msg_id = query.message.message_id

        if query.data == 'main_image':
            reply_markup = tg.InlineKeyboardMarkup(self.image_menu)
            query.message.edit_text(text='Choose your Poison :', reply_markup=reply_markup)

        elif query.data == 'main_text':
            reply_markup = tg.InlineKeyboardMarkup(self.text_menu)
            query.message.edit_text(text='Choose your Poison :', reply_markup=reply_markup)

        elif query.data == 'main_tools':
            reply_markup = tg.InlineKeyboardMarkup(self.tool_menu)
            query.message.edit_text(text='What can I help you with? :', reply_markup=reply_markup)

        elif query.data == 'main_back':
            reply_markup = tg.InlineKeyboardMarkup(self.main_menu)
            query.message.edit_text(text='What can I help you with? :', reply_markup=reply_markup)
        
        elif query.data == 'main_cancel':
            context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            context.bot.send_message(chat_id=chat_id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

    def img_actions(self, update, context):
        query = update.callback_query
        chat_id = query.message.chat.id
        msg_id = query.message.message_id

        context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'img_meme':
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

        if query.data == 'img_doggo':
            doggo = requests.get(DOG_PIC_URL).json()['message']
            try:
                caption = "Dog Fact - "+requests.get(DOG_CAP_URL).json()[0]['fact']
            except:
                caption = "Dog Fact - "+"Random Dog Fact expected here. Error occured"
            context.bot.send_photo(chat_id=chat_id, photo=doggo, caption=caption)

        if query.data == 'img_kitty':
            kitty = requests.get(CAT_PIC_URL).json()['url']
            try:
                caption = "Cat Fact - "+requests.get(CAT_CAP_URL).json()['text']
            except:
                caption = "Cat Fact - "+"Random Cat Fact expected here. Error occured"
            context.bot.send_photo(photo=kitty, caption=caption, chat_id=chat_id)

        if query.data == 'img_human':
            msg = "This person does not exist. \nIt was imagined by a GAN (Generative Adversarial Network) \n\nReference - [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com)"

            im = Image.open(requests.get(RANDOM_HUMAN_URL, stream=True).raw)
            im.save('static/person.png', 'PNG')

            context.bot.send_photo(photo=open('static/person.png', 'rb'), caption=msg, chat_id=chat_id, parse_mode="Markdown")

        if query.data == 'img_namo':
            response = requests.get(NAMO_URL).json()[0]
            meme = response["url"]
            context.bot.send_photo(chat_id=chat_id, photo=meme, caption="NaMo 🙏🏻", parse_mode="Markdown")

        if query.data == 'img_hero':
            try:
                response = requests.get(HERO_CDN_URL+'{}.json'.format(random.choice(HERO_IDS))).json()
            except:
                response = requests.get(HERO_BASE_URL+'{}.json'.format(random.choice(HERO_IDS))).json()
            
            caption = HERO_MSG.format(response['name'], *response['powerstats'].values(), *response['appearance'].values(), response['work']['occupation'], *response['biography'].values())
            context.bot.send_photo(chat_id=chat_id, photo=response['images']['lg'], caption=caption, parse_mode="Markdown")
        
        self.update_chat(context, chat_id, self.image_menu)

    def txt_actions(self, update, context):
        query = update.callback_query
        chat_id = query.message.chat.id
        msg_id = query.message.message_id

        context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'txt_quote':
            response = requests.get(QUOTE_URL).json()
            msg = "_{}_ \n\n- {}".format(response['content'], response['author'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

        if query.data == 'txt_kanye':
            response = requests.get(KANYE_URL).json()
            msg = "Kanye REST once said, \n\n_{}_".format(response['quote'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            
        if query.data == 'txt_trump':
            response = requests.get(TRUMP_URL).json()
            msg = "Grumpy Donald once said, \n\n_{}_".format(response['message'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        
        if query.data == 'txt_daily':
            response = requests.get(DAILY_URL).json()
            msg = "Bored out your mind? \nI can suggest you something to try something out. \n\nActivity - *{}*\nType - *{}*\nParticipants Suggested - *{}*\n\n_Take it as a challenge ;)_".format(response["activity"], response["type"], response["participants"])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

        if query.data == 'txt_facts':
            response = requests.get(FACTS_URL).json()
            msg = "Did you know, \n\n_{}_".format(response['text'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        
        if query.data == 'txt_poems':
            response = random.choice(requests.get(POEMS_URL).json())
            msg = "*{}* \n\n{} \n\nBy *{}*".format(response['title'], response['content'], response['poet']['name'])
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        
        self.update_chat(context, chat_id, self.text_menu)

    def exe_actions(self, update, context):
        query = update.callback_query
        chat_id = query.message.chat.id
        msg_id = query.message.message_id

        context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'exe_rdm':
            rdm = requests.get(RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]

            msg = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            
        if query.data == 'exe_pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

            text = "Here's your password.\nClick on the password to copy.\n\n`{}`".format(pwd)
            context.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

        if query.data == 'exe_age':
            name = query.message.chat.first_name
            age = str(requests.get(AGE_URL+"?name={}".format(name)).json()['age'])

            msg = "Based on my knowledge, I think a person with the name {} would be {} years old \nI might be wrong tho :') \n\nReference: [Agify.io](https://agify.io/) \n\n_Agify predicts the age of a person given their name based on analytics, ad segmenting, demographic statistics etc._".format(name, age)
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown", disable_web_page_preview=True)
        
        if query.data == 'exe_web':
            msg = USEFUL_WEBSITE_URL
            context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown", disable_web_page_preview=True)
        
        self.update_chat(context, chat_id, self.tool_menu)

    def dev(self, update, context):
        info = "Made with Py3 and AIML. \nFor any queries contact, [a_ignorant_mortal](https://t.me/a_ignorant_mortal) \n\nMore about the dev: [Linktree](https://linktr.ee/ign_mortal)"
        update.message.reply_text(info, parse_mode="Markdown")

    def slap(self, update, context):
        chat_id = update.message.chat.id
        mention = update.message.text[5:].strip()
        # user_id = int(str(update).split("'id': ")[-1].split(',')[0])
        # user_id = int(re.findall(r'[0-9]+', str(update.message))[-1])
        user_id = update.message.from_user.id

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
        text = "Hmmm. Something went wrong. \n\nThis wasn't supposed to happen though. Please try something else while we look into it. ʘ‿ʘ"
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=text, show_alert=True)


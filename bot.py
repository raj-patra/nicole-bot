import logging, os, aiml, requests, random, string
import telegram as tg

from PIL import Image
from bs4 import BeautifulSoup
from helpers.constants import *
from helpers.urls import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


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

        self.kernel.setPredicate("name", "Stranger")
        self.logger = logging.getLogger(__name__)

        self.main_menu =tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Image APIs 🌆', callback_data="main_image"), tg.InlineKeyboardButton('Text APIs 📝', callback_data="main_text")],
                            [tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_tools")],
                            [tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.image_menu=tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Reddit Guild 🤙', callback_data='img_meme'), tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='img_namo')],
                            [tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='img_hero')],
                            [tg.InlineKeyboardButton('Cute Doggo 🐶', callback_data='img_doggo'), tg.InlineKeyboardButton('Little Kitty 🐱', callback_data='img_kitty')],
                            [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='img_human')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.text_menu =tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Quote of the Day 💯', callback_data='txt_quote'), tg.InlineKeyboardButton('Fact of the Day 🤯', callback_data='txt_facts')],
                            [tg.InlineKeyboardButton('A Literati\'s Wet Dream 🎶', callback_data='txt_poems')],
                            [tg.InlineKeyboardButton('Kanye REST 🧭', callback_data='txt_kanye'), tg.InlineKeyboardButton('Donald Grump 🎺', callback_data='txt_trump')], 
                            [tg.InlineKeyboardButton('Blesseth Thee Shakespeare 🤡', callback_data='txt_shake')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.tool_menu =tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Spotify Premium Mod 💚', callback_data='exe_mod')],
                            [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='exe_rdm'), tg.InlineKeyboardButton('Useful Websites </>', callback_data='exe_web')],
                            [tg.InlineKeyboardButton('10 Digit Password Generator', callback_data='exe_pwd')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])

    def __str__(self):
        return "Nicole, is a conversational chatbot made to serve as a telegram client side bot."

    def start(self, update, context):
        reply_markup = self.main_menu
        intro = """Hi! I am *Nicole*, a conversational chatbot. \n\nUse the /menu for tools or send a text to chat. \nGLHF"""
        menu = "Choose your poison: "
        if "/menu" in update.message.text:
            update.message.reply_photo(photo=NICOLE_DP_URL, caption=menu, reply_markup=reply_markup)
        elif "/start"in update.message.text:
            update.message.reply_text(intro, parse_mode="Markdown")

    def menu_actions(self, update, context):
        query = update.callback_query

        if query.data == 'main_image':
            query.message.edit_reply_markup(self.image_menu)

        elif query.data == 'main_text':
            query.message.edit_reply_markup(self.text_menu)

        elif query.data == 'main_tools':
            query.message.edit_reply_markup(self.tool_menu)

        elif query.data == 'main_back':
            query.message.edit_reply_markup(self.main_menu)

        elif query.data == 'main_cancel':
            context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
            context.bot.send_message(chat_id=query.message.chat.id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

    def img_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.image_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'img_meme':
            response = requests.get(MEME_URL).json()
            media = response["url"]
            caption = """*{}* \n\nPosted in [r/{}](www.reddit.com/r/{}) by [u/{}](www.reddit.com/user/{}) \nLink - {}
            
            """.format(response['title'], response['subreddit'], response['subreddit'], response['author'], response['author'], response['postLink'])

            if response['nsfw'] == True:
                caption += "#nsfw"
            if response['spoiler'] == True:
                caption += "#spolier"

        if query.data == 'img_doggo':
            media = requests.get(DOG_PIC_URL).json()['message']
            try:
                caption = "Dog Fact - "+requests.get(DOG_CAP_URL).json()[0]['fact']
            except:
                caption = "Dog Fact - "+"Random Dog Fact expected here. Error occured"

        if query.data == 'img_kitty':
            media = requests.get(CAT_PIC_URL).json()['url']
            try:
                caption = "Cat Fact - "+requests.get(CAT_CAP_URL).json()['text']
            except:
                caption = "Cat Fact - "+"Random Cat Fact expected here. Error occured"

        if query.data == 'img_human':
            im = Image.open(requests.get(RANDOM_HUMAN_URL, stream=True).raw)
            im.save('static/person.png', 'PNG')

            media = open('static/person.png', 'rb')
            caption = "This person does not exist. \nIt was imagined by a GAN (Generative Adversarial Network) \n\nReference - [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com)"

        if query.data == 'img_namo':
            response = requests.get(NAMO_URL).json()[0]
            media = response["url"]
            caption = "NaMo 🙏🏻"

        if query.data == 'img_hero':
            try:
                response = requests.get(HERO_CDN_URL+'{}.json'.format(random.choice(HERO_IDS))).json()
            except:
                response = requests.get(HERO_BASE_URL+'{}.json'.format(random.choice(HERO_IDS))).json()

            media = response['images']['lg']
            caption = HERO_MSG.format(response['name'], *response['powerstats'].values(), *response['appearance'].values(), response['work']['occupation'], *response['biography'].values())

        query.message.edit_media(tg.InputMediaPhoto(media=media, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)
        
    def txt_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.text_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'txt_quote':
            response = requests.get(QUOTE_URL).json()
            text = "*{}* \n\n- {}".format(response['content'], response['author'])

        if query.data == 'txt_kanye':
            response = requests.get(KANYE_URL).json()
            text = "Kanye REST once said, \n\n*{}*".format(response['quote'])
            
        if query.data == 'txt_trump':
            response = requests.get(TRUMP_URL).json()
            text = "Grumpy Donald once said, \n\n*{}*".format(response['message'])
        
        if query.data == 'txt_shake':
            response = requests.get(SHAKE_URL).json()
            text = "*{}* \n\n{}\n#{}".format(response['quote']['quote'], response["quote"]["play"], response["quote"]["theme"])

        if query.data == 'txt_facts':
            response = requests.get(FACTS_URL).json()
            text = "Did you know, \n\n*{}*".format(response['text'])
        
        if query.data == 'txt_poems':
            response = random.choice(requests.get(POEMS_URL).json())
            text = "*{}* \n\n{} \n\nBy *{}*".format(response['title'], response['content'], response['poet']['name'])
        
        query.message.edit_media(tg.InputMediaPhoto(media=NICOLE_DP_URL, caption=text, parse_mode="Markdown"), reply_markup=reply_markup)
        
    def exe_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.tool_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'exe_rdm':
            rdm = requests.get(RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]
            text = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)
            media = tg.InputMediaPhoto(media=NICOLE_DP_URL, caption=text, parse_mode="Markdown")
            
        if query.data == 'exe_pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            text = "Here's your password.\nClick on the password to copy.\n\n`{}`".format(pwd)
            media = tg.InputMediaPhoto(media=NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        if query.data == 'exe_mod':
            media = tg.InputMediaDocument(media=SPOTIFY_MOD, caption=SPOTIFY_CAP, parse_mode="Markdown")
        
        if query.data == 'exe_web':
            text = USEFUL_WEBSITE_MSG
            media = tg.InputMediaPhoto(media=NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        query.message.edit_media(media=media, reply_markup=reply_markup)

    def respond(self, update, context):
        if update.message.chat.type == 'private':
            update.message.reply_text(self.kernel.respond(update.message.text))

        elif update.message.reply_to_message:
            if update.message.reply_to_message.from_user.username == 'a_ignorant_mortal_bot':
                update.message.reply_text(self.kernel.respond(update.message.text))

    def error(self, update, context):
        self.logger.warning('Update that caused the error, \n\n"%s" \n\nThe Error "%s"', update, context.error)
        text = "Hmmm. Something went wrong. \n\nThis wasn't supposed to happen though. Please try something else while we look into it. ʘ‿ʘ"
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=text, show_alert=True)
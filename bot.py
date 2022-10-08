import logging
import os
import random
import string

import aiml
import requests
import telegram as tg
from bs4 import BeautifulSoup

from handler import CHandler
from helpers import constants, urls
from helpers.actions import ImageActions, TextActions

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class NicoleBot:

    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.verbose(0)
        self.kernel.setBotPredicate("name", "Nicole")

        # Load/Learn Brain file
        if os.path.isfile("static/bot_brain.brn"):
            self.kernel.bootstrap(brainFile="static/bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
            self.kernel.saveBrain("static/bot_brain.brn")

        self.kernel.setPredicate("name", "Stranger")
        self.logger = logging.getLogger(__name__)

        self.image_reqs = ImageActions()
        self.text_reqs = TextActions()

        self.main_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Quizzeria 💡', callback_data="main_quiz")],
                [tg.InlineKeyboardButton('Visuals 🌆', callback_data="main_image"),tg.InlineKeyboardButton('Quotify 📝', callback_data="main_quote")],
                [tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_tools")],
                [tg.InlineKeyboardButton('Trivia 🔀', callback_data="main_trivia"),tg.InlineKeyboardButton('Recreation 🥳', callback_data="main_joke")],
                [tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.image_menu= tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='image_namo')],
                [tg.InlineKeyboardButton('Reddit Guild 🤙', callback_data='image_meme'),tg.InlineKeyboardButton('Inspire Robot 🎇', callback_data='image_inspire')],
                [tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='image_hero')],
                [tg.InlineKeyboardButton('Nat Geo 🌏', callback_data='image_animal'),tg.InlineKeyboardButton('Asciify 🧑', callback_data='image_asciify')],
                [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='image_human')],
                [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'),tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.quote_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Random Quotes 💯', callback_data='quote_popular'),],
                [tg.InlineKeyboardButton('Stoicism 🦾', callback_data='quote_stoic'),tg.InlineKeyboardButton('Free Advice 🆓', callback_data='quote_advice')],
                [tg.InlineKeyboardButton('Build Morale 😇', callback_data='quote_affirmation')],
                [tg.InlineKeyboardButton('Super Hero 🦸‍♂️🦸‍♀️', callback_data='quote_heros'),tg.InlineKeyboardButton('Anime Chan 🗯', callback_data='quote_anime')],
                [tg.InlineKeyboardButton('Stay Inspired 🐱‍👤', callback_data='quote_inspire')],
                [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'),tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.joke_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Dad Energy 🧔', callback_data='joke_dad'),tg.InlineKeyboardButton('Yo Momma 🤶', callback_data='joke_mom')],
                [tg.InlineKeyboardButton('Roast Me 🔥', callback_data='joke_roast')],
                [tg.InlineKeyboardButton('Kanye West 🧭', callback_data='joke_kanye'),tg.InlineKeyboardButton('Donald Trump 🎺', callback_data='joke_trump')],
                [tg.InlineKeyboardButton('Chuck Norris 😈', callback_data='joke_chuck')],
                [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'),tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.trivia_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Useless Facts 🤯', callback_data='trivia_facts'),tg.InlineKeyboardButton('Good Reads 🎶', callback_data='trivia_poems')],
                [tg.InlineKeyboardButton('Number Trivia 🔢', callback_data='trivia_number')],
                [tg.InlineKeyboardButton('Date Trivia 📆', callback_data='trivia_date'),tg.InlineKeyboardButton('Year Trivia 📅', callback_data='trivia_year'),],
                [tg.InlineKeyboardButton('Math Trivia ➕', callback_data='trivia_math')],
                [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'),tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.tool_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='exe_rdm'),tg.InlineKeyboardButton('Useful Websites </>', callback_data='exe_web')],
                [tg.InlineKeyboardButton('Spotify Premium Mod 💚', callback_data='exe_mod')],
                [tg.InlineKeyboardButton('Password Generator', callback_data='exe_pwd'),tg.InlineKeyboardButton('Alias Generator', callback_data='exe_alias')],
                [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'),tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel')]
            ]
        )
        self.quiz_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Let Fate Decide 🔀', callback_data='quiz_random')],
                [tg.InlineKeyboardButton('Beginner 🟢', callback_data='quiz_easy'),tg.InlineKeyboardButton('No Mercy 🟡', callback_data='quiz_medium')],
                [tg.InlineKeyboardButton('Soul Crushing 🔴', callback_data='quiz_hard')],
                [tg.InlineKeyboardButton('Main Menu', callback_data='quiz_menu'),tg.InlineKeyboardButton('Give Up 🙉', callback_data='main_cancel')]
            ]
        )


    def __str__(self):
        return "Nicole, is a conversational chatbot made to serve as a telegram client side bot."

    def start(self, update, context):

        reply_markup = self.main_menu
        intro = constants.INTRO_TXT.format("-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)]))
        menu = "Choose your poison: "

        if "/menu" in update.message.text:
            update.message.reply_photo(photo=urls.NICOLE_DP_URL, caption=menu, reply_markup=reply_markup)
        elif "/start"in update.message.text:
            update.message.reply_text(intro, parse_mode="Markdown")

    def menu_actions(self, update, context):

        query = update.callback_query

        if query.data == 'main_image':
            query.message.edit_reply_markup(self.image_menu)

        elif query.data == 'main_tools':
            query.message.edit_reply_markup(self.tool_menu)

        elif query.data == 'main_quote':
            query.message.edit_reply_markup(self.quote_menu)

        elif query.data == 'main_joke':
            query.message.edit_reply_markup(self.joke_menu)

        elif query.data == 'main_trivia':
            query.message.edit_reply_markup(self.trivia_menu)

        elif query.data == 'main_quiz':
            query.message.edit_reply_markup(self.quiz_menu)

        elif query.data == 'main_back':
            query.message.edit_reply_markup(self.main_menu)

        elif query.data == 'main_cancel':
            context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
            context.bot.send_message(chat_id=query.message.chat.id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

    def image_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.image_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'image_meme':
            media, caption, error = self.image_reqs.get_meme()

        if query.data == 'image_animal':
            media, caption, error = self.image_reqs.get_animal()

        if query.data == 'image_asciify':
            user_dp = CHandler().get_dp(query.from_user.id, context)
            media, caption, error = self.image_reqs.get_asciify(user_dp)
            user_dp.close()

        if query.data == 'image_human':
            media, caption, error = self.image_reqs.get_human()

        if query.data == 'image_namo':
            media, caption, error = self.image_reqs.get_namo()

        if query.data == 'image_hero':
            media, caption, error = self.image_reqs.get_hero()

        if query.data == 'image_inspire':
            media, caption, error = self.image_reqs.get_inspire()

        if error:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            query.message.edit_media(tg.InputMediaPhoto(media=media, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

        if os.path.exists('static/output.png'):
            media.close()
            os.remove('static/output.png')

    def quote_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.quote_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_quote(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    def joke_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.joke_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_joke(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    def trivia_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.trivia_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_trivia(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    def quiz_actions(self, update, context):

        query = update.callback_query
        chat_id = query.message.chat.id

        if query.data == 'quiz_menu':
            if query.message.poll == None:
                query.message.edit_reply_markup(self.main_menu)
            else:
                context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
                context.bot.send_photo(chat_id=query.message.chat.id, photo=urls.NICOLE_DP_URL, caption="Choose your poison: ", reply_markup=self.main_menu)
        else:
            reply_markup = self.quiz_menu
            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

            response = requests.get(urls.QUIZ_API[query.data]["url"]).json()['results'][0]

            category, question = response['category'], response['question']
            correct_answer, incorrect_answers = response['correct_answer'], response['incorrect_answers']

            def escape(text):
                """HTML-escape the text in `t`."""
                return (text
                    .replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&#39;", "'").replace("&quot;", '"')
                    )

            question = escape(question)
            answers = incorrect_answers + [correct_answer]
            answers = [escape(item) for item in answers]
            random.shuffle(answers)
            correct_answer_index = answers.index(correct_answer)

            context.bot.send_poll(
                chat_id=chat_id,
                question=question,
                options=answers,
                type=tg.Poll.QUIZ,
                correct_option_id=correct_answer_index,
                open_period=urls.QUIZ_API[query.data]["timer"],
                is_anonymous=True,
                explanation="Category : *{}*".format(category),
                explanation_parse_mode=tg.ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )

    def exe_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.tool_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'exe_rdm':
            rdm = requests.get(urls.RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]
            text = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)

        elif query.data == 'exe_pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            text = "*Here's your password. Click to copy.*\n\n`{}`".format(pwd)

        elif query.data == 'exe_alias':
            alias = "-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)])
            text = "*Here's your alias. Click to copy*.\n\n`{}`".format(alias)

        elif query.data == 'exe_web':
            text = constants.USEFUL_WEBSITE_MSG

        if query.data == 'exe_mod':
            media = tg.InputMediaDocument(media=constants.SPOTIFY_MOD, caption=constants.SPOTIFY_CAP, parse_mode="Markdown")
        else:
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        query.message.edit_media(media=media, reply_markup=reply_markup)

    def respond(self, update, context):

        if update.message:
            query = update.message
        elif update.edited_message:
            query = update.edited_message

        first_name, last_name, user_name, user_id = query.from_user.first_name, \
            query.from_user.last_name, query.from_user.username, \
                query.from_user.id

        text, is_bot, chat_id, chat_type = query.text, \
            query.from_user.is_bot, query.chat.id, \
                query.chat.type

        if query.chat.type == 'private':
            title = query.chat.username
            query.reply_text(self.kernel.respond(text))
        else:
            title = query.chat.title

        QUERY = constants.MESSAGE_QUERY.format(title, chat_type, chat_id, text, \
                first_name, last_name, user_name, user_id)

        if query.reply_to_message:
            if query.reply_to_message.from_user.username == 'a_ignorant_mortal_bot':
                query.reply_text(self.kernel.respond(query.text))
            else:
                pass #In groups, Nicole will reply if someone replies to its message

        if chat_id != constants.EXCEMPT_GROUP:
            context.bot.send_message(chat_id=constants.DATABASE_GROUP, text=QUERY, parse_mode="Markdown")

    def error(self, update, context):

        self.logger.warning('Update that caused the error, \n\n"%s" \n\nThe Error "%s"', update, context.error)
        if update.callback_query.id:
            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=constants.ERROR_TXT, show_alert=True)

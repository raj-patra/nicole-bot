import logging
import os
import random
import string

import aiml
import requests
import telegram as tg
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes

from handler import CHandler
from helpers import constants, urls
from helpers.actions import ImageActions, TextActions
from helpers.menus import MENUS

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
                [MENUS["main_quiz"]],
                [MENUS["main_visuals"], MENUS["main_quotify"]],
                [MENUS["main_service"]],
                [MENUS["main_trivia"], MENUS["main_recreation"]],
                [MENUS["cancel"]],
            ]
        )
        self.image_menu= tg.InlineKeyboardMarkup(
            [
                [MENUS["visuals_animal"], MENUS["visuals_inspire"]],
                [MENUS["visuals_hero"]],
                [MENUS["back"], MENUS["cancel"]],
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
        self.service_menu = tg.InlineKeyboardMarkup(
            [
                [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='service_bored'),tg.InlineKeyboardButton('Useful Websites </>', callback_data='service_web')],
                [tg.InlineKeyboardButton('Spotify Premium Mod 💚', callback_data='service_mod')],
                [tg.InlineKeyboardButton('Password Generator', callback_data='service_pwd'),tg.InlineKeyboardButton('Alias Generator', callback_data='service_alias')],
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

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        reply_markup = self.main_menu
        intro = constants.INTRO_TXT.format("-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)]))
        menu = "Choose your poison: "

        if "/menu" in update.message.text:
            await update.message.reply_photo(photo=urls.NICOLE_DP_URL, caption=menu, reply_markup=reply_markup)
        elif "/start"in update.message.text:
            await update.message.reply_text(intro, parse_mode="Markdown")

    async def menu_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query

        if query.data == 'main_image':
            await query.message.edit_reply_markup(self.image_menu)

        elif query.data == 'main_service':
            await  query.message.edit_reply_markup(self.service_menu)

        elif query.data == 'main_quote':
            await  query.message.edit_reply_markup(self.quote_menu)

        elif query.data == 'main_joke':
            await  query.message.edit_reply_markup(self.joke_menu)

        elif query.data == 'main_trivia':
            await  query.message.edit_reply_markup(self.trivia_menu)

        elif query.data == 'main_quiz':
            await  query.message.edit_reply_markup(self.quiz_menu)

        elif query.data == 'main_back':
            await  query.message.edit_reply_markup(self.main_menu)

        elif query.data == 'main_cancel':
            await  context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
            await  context.bot.send_message(chat_id=query.message.chat.id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

    async def image_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.image_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'image_animal':
            media, caption, error = self.image_reqs.get_animal()

        if query.data == 'image_inspire':
            media, caption, error = self.image_reqs.get_inspire()

        if query.data == 'image_hero':
            media, caption, error = self.image_reqs.get_hero()

        if error:
            await query.message.edit_media(tg.InputMediaPhoto(
                media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, 
                parse_mode=tg.constants.ParseMode.MARKDOWN), reply_markup=reply_markup
            )
        else:
            await query.message.edit_media(tg.InputMediaPhoto(
                media=media, caption=caption, 
                parse_mode=tg.constants.ParseMode.MARKDOWN), reply_markup=reply_markup
            )

    async def quote_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.quote_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_quote(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def joke_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.joke_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_joke(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def trivia_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.trivia_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_trivia(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()['image']
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def quiz_actions(self, update, context):

        query = update.callback_query
        chat_id = query.message.chat.id

        if query.data == 'quiz_menu':
            if query.message.poll == None:
                await query.message.edit_reply_markup(self.main_menu)
            else:
                await context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
                await context.bot.send_photo(chat_id=query.message.chat.id, photo=urls.NICOLE_DP_URL, caption="Choose your poison: ", reply_markup=self.main_menu)
        else:
            reply_markup = self.quiz_menu
            await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

            response = requests.get(urls.QUIZ_API[query.data]["url"]).json()['results'][0]

            category, question = response['category'], response['question']
            answers = [response['correct_answer']] + response['incorrect_answers']
            random.shuffle(answers)
            correct_answer_index = answers.index(response['correct_answer'])

            def escape(text):
                """HTML-escape the text in `t`."""
                return (text
                    .replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&#039;", "'").replace("&quot;", '"')
                    )

            question = escape(question)
            answers = [escape(item) for item in answers]

            await context.bot.send_poll(
                chat_id=chat_id, type=tg.Poll.QUIZ,
                question=question, options=answers, correct_option_id=correct_answer_index,
                open_period=urls.QUIZ_API[query.data]["timer"], is_anonymous=True,
                explanation="Category : *{}*".format(category),
                explanation_parse_mode=tg.constants.ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )

    async def service_actions(self, update, context):

        query = update.callback_query
        reply_markup = self.service_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == 'service_bored':
            rdm = requests.get(urls.RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+'\n'+soup.find("iframe")["src"]
            text = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)

        elif query.data == 'service_pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            text = "*Here's your password. Click to copy.*\n\n`{}`".format(pwd)

        elif query.data == 'service_alias':
            alias = "-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)])
            text = "*Here's your alias. Click to copy*.\n\n`{}`".format(alias)

        elif query.data == 'service_web':
            text = constants.USEFUL_WEBSITE_MSG

        if query.data == 'service_mod':
            media = tg.InputMediaDocument(media=constants.SPOTIFY_MOD, caption=constants.SPOTIFY_CAP, parse_mode="Markdown")
        else:
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        await query.message.edit_media(media=media, reply_markup=reply_markup)

    async def respond(self, update, context):

        if update.message:
            query = update.message
        elif update.edited_message:
            query = update.edited_message

        first_name, last_name, user_name, user_id = query.from_user.first_name, \
            query.from_user.last_name, query.from_user.username, \
                query.from_user.id

        stimulus, is_bot, chat_id, chat_type = query.text, \
            query.from_user.is_bot, query.chat.id, \
                query.chat.type

        # Nicole replies if DMed privately or replied to in a group
        if query.chat.type == 'private' or (query.reply_to_message and query.reply_to_message.from_user.username == 'a_ignorant_mortal_bot'):
            title = query.chat.title or query.chat.username or first_name+' '+last_name
            response = self.kernel.respond(stimulus)
            await query.reply_text(response)

            if chat_id != constants.EXCEMPT_GROUP:
                QUERY = constants.MESSAGE_QUERY.format(stimulus, response,\
                    first_name, last_name, user_name, user_id, title, chat_type, chat_id)
                await context.bot.send_message(chat_id=constants.DATABASE_GROUP, text=QUERY, parse_mode="Markdown")

    async def error(self, update, context):

        self.logger.warning('Update that caused the error, \n\n"%s" \n\nThe Error "%s"', update, context.error)
        if update.callback_query.id:
            await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=constants.ERROR_TXT, show_alert=True)

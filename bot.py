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

from helpers import constants, menus, urls
from helpers.actions import ImageActions, TextActions

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


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

        self.main_menu = menus.MAIN_MENU
        self.quiz_menu = menus.QUIZ_MENU
        self.image_menu= menus.VISUALS_MENU
        self.quote_menu = menus.QUOTES_MENU
        self.joke_menu = menus.RECREATION_MENU
        self.trivia_menu = menus.TRIVIA_MENU
        self.service_menu = menus.SERVICE_MENU

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

        if query.data == "main_image":
            await query.message.edit_reply_markup(self.image_menu)

        elif query.data == "main_service":
            await  query.message.edit_reply_markup(self.service_menu)

        elif query.data == "main_quote":
            await  query.message.edit_reply_markup(self.quote_menu)

        elif query.data == "main_joke":
            await  query.message.edit_reply_markup(self.joke_menu)

        elif query.data == "main_trivia":
            await  query.message.edit_reply_markup(self.trivia_menu)

        elif query.data == "main_quiz":
            await  query.message.edit_reply_markup(self.quiz_menu)

    async def visual_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        reply_markup = self.image_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == "visual_animal":
            media, caption, error = self.image_reqs.get_animal()

        if query.data == "visual_inspire":
            media, caption, error = self.image_reqs.get_inspire()

        if query.data == "visual_hero":
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

    async def quote_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        reply_markup = self.quote_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_quote(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def recreation_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        reply_markup = self.joke_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_recreation(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def trivia_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        reply_markup = self.trivia_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = self.text_reqs.get_trivia(query.data)

        if error:
            reaction = requests.get(urls.NO_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            reaction = requests.get(urls.YES_RXN).json()["image"]
            await query.message.edit_media(tg.InputMediaVideo(media=reaction, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)

    async def quiz_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        chat_id = query.message.chat.id

        if query.data == "quiz_menu":
            if query.message.poll == None:
                await query.message.edit_reply_markup(self.main_menu)
            else:
                await context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
                await context.bot.send_photo(chat_id=query.message.chat.id, photo=urls.NICOLE_DP_URL, caption="Choose your poison: ", reply_markup=self.main_menu)
        else:
            reply_markup = self.quiz_menu
            await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

            response = requests.get(urls.QUIZ_API[query.data]["url"]).json()["results"][0]

            category, question = response["category"], response["question"]
            answers = [response["correct_answer"]] + response["incorrect_answers"]
            random.shuffle(answers)
            correct_answer_index = answers.index(response["correct_answer"])

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

    async def service_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        reply_markup = self.service_menu
        await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        if query.data == "service_bored":
            rdm = requests.get(urls.RANDOM_WEBSITE_URL)
            soup = BeautifulSoup(rdm.text, features="html.parser")
            site = soup.find("iframe")["title"]+"\n"+soup.find("iframe")["src"]
            text = "This is the bored button, an archive of internet's most useless websites curated to cure you of your boredom. \n\n*{}*\n\nFor best results, use a PC.".format(site)

        elif query.data == "service_pwd":
            pwd = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            text = "*Here's your password. Click to copy.*\n\n`{}`".format(pwd)

        elif query.data == "service_alias":
            alias = "-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)])
            text = "*Here's your alias. Click to copy*.\n\n`{}`".format(alias)

        elif query.data == "service_web":
            text = constants.USEFUL_WEBSITE_MSG

        if query.data == "service_mod":
            media = tg.InputMediaDocument(media=constants.SPOTIFY_MOD, caption=constants.SPOTIFY_CAP, parse_mode="Markdown")
        else:
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        await query.message.edit_media(media=media, reply_markup=reply_markup)

    async def misc_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query

        if query.data == "misc_back":
            await  query.message.edit_reply_markup(self.main_menu)

        elif query.data == "misc_cancel":
            await  context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
            await  context.bot.send_message(chat_id=query.message.chat.id, text="Sure, I wasn't doing anything anyway. ¯\_ಠಿ‿ಠ_/¯")

    async def respond(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

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
        if query.chat.type == "private" or (query.reply_to_message and query.reply_to_message.from_user.username == "a_ignorant_mortal_bot"):
            title = query.chat.title or query.chat.username or first_name+" "+last_name
            response = self.kernel.respond(stimulus)
            await query.reply_text(response)

            if chat_id != constants.EXCEMPT_GROUP:
                QUERY = constants.MESSAGE_QUERY.format(stimulus, response,\
                    first_name, last_name, user_name, user_id, title, chat_type, chat_id)
                await context.bot.send_message(chat_id=constants.DATABASE_GROUP, text=QUERY, parse_mode="Markdown")

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        self.logger.warning('Update that caused the error, \n\n"%s" \n\nThe Error "%s"', update, context.error)
        if update.callback_query.id:
            await context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=constants.ERROR_TXT, show_alert=True)

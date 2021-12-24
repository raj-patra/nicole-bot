import logging
import os
import random
import string

import aiml
import requests
import telegram as tg
from bs4 import BeautifulSoup
from PIL import Image

from handler import CHandler
from helpers import constants, urls
from helpers.api import (get_animal, get_asciify, get_caption, get_fun_caption,
                         get_hero, get_human, get_inspire, get_meme, get_namo,
                         get_rdm_caption)

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

        self.main_menu = tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Quizzeria 💡', callback_data="main_quiz")],
                            [tg.InlineKeyboardButton('Quotify 📝', callback_data="main_text"), tg.InlineKeyboardButton('Trivia 🔀', callback_data="main_random")],
                            [tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_tools")],
                            [tg.InlineKeyboardButton('Visuals 🌆', callback_data="main_image"), tg.InlineKeyboardButton('Recreation 🥳', callback_data="main_fun")],
                            [tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.image_menu= tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Inspire Robot 🎇', callback_data='img_inspire')],
                            [tg.InlineKeyboardButton('Reddit Guild 🤙', callback_data='img_meme'), tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='img_namo')],
                            [tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='img_hero')],
                            [tg.InlineKeyboardButton('Nat Geo 🌏', callback_data='img_animal'), tg.InlineKeyboardButton('Asciify 🧑', callback_data='img_asciify')],
                            [tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='img_human')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.text_menu = tg.InlineKeyboardMarkup([
                            [
                                tg.InlineKeyboardButton('Random Quotes 💯', callback_data='txt_quote'), \
                            ],
                            [
                                tg.InlineKeyboardButton('Stoicism 🦾', callback_data='txt_stoic'), \
                                tg.InlineKeyboardButton('Free Advice 🆓', callback_data='txt_advice')
                            ],
                            [
                                tg.InlineKeyboardButton('Build Morale 😇', callback_data='txt_affirmation')
                            ],
                            [
                                tg.InlineKeyboardButton('Super Hero 🦸‍♂️🦸‍♀️', callback_data='txt_heros'), \
                                tg.InlineKeyboardButton('Anime Chan 🗯', callback_data='txt_anime')
                            ],
                            [
                                tg.InlineKeyboardButton('Stay Inspired 🐱‍👤', callback_data='txt_inspire')
                            ],
                            [
                                tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), \
                                tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')
                            ]
                        ])
        self.fun_menu = tg.InlineKeyboardMarkup([
                            [
                                tg.InlineKeyboardButton('Kanye West 🧭', callback_data='fun_kanye'), \
                                tg.InlineKeyboardButton('Donald Trump 🎺', callback_data='fun_trump')
                            ],
                            [
                                tg.InlineKeyboardButton('Roast Me 🔥', callback_data='fun_roast')
                            ],
                            [
                                tg.InlineKeyboardButton('Dad Energy 🧔', callback_data='fun_dad'), \
                                tg.InlineKeyboardButton('Yo Momma 🤶', callback_data='fun_mom')
                            ],
                            [
                                tg.InlineKeyboardButton('Chuck Norris 😈', callback_data='fun_chuck')
                            ],
                            [
                                tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), \
                                tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')
                            ]
                        ])
        self.random_menu = tg.InlineKeyboardMarkup([
                            [
                                tg.InlineKeyboardButton('Useless Facts 🤯', callback_data='rdm_facts'), \
                                tg.InlineKeyboardButton('Good Reads 🎶', callback_data='rdm_poems')
                            ],
                            [
                                tg.InlineKeyboardButton('Number Trivia 🔢', callback_data='rdm_number')
                            ],
                            [
                                tg.InlineKeyboardButton('Date Trivia 📆', callback_data='rdm_date'), \
                                tg.InlineKeyboardButton('Year Trivia 📅', callback_data='rdm_year'), \
                            ],
                            [
                                tg.InlineKeyboardButton('Math Trivia ➕', callback_data='rdm_math')
                            ],
                            [
                                tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), \
                                tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')
                            ]
                        ]) 
        self.tool_menu = tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Bored Button 🥱', callback_data='exe_rdm'), tg.InlineKeyboardButton('Useful Websites </>', callback_data='exe_web')],
                            [tg.InlineKeyboardButton('Spotify Premium Mod 💚', callback_data='exe_mod')],
                            [tg.InlineKeyboardButton('Password Generator', callback_data='exe_pwd'), tg.InlineKeyboardButton('Alias Generator', callback_data='exe_alias')],
                            [tg.InlineKeyboardButton('◀ Back', callback_data='main_back'), tg.InlineKeyboardButton('Cancel Op ❌', callback_data='main_cancel')]
                        ])
        self.quiz_menu = tg.InlineKeyboardMarkup([
                            [tg.InlineKeyboardButton('Let Fate Decide 🔀', callback_data='quiz_random')],
                            [tg.InlineKeyboardButton('Beginner 🟢', callback_data='quiz_easy'), tg.InlineKeyboardButton('No Mercy 🟡', callback_data='quiz_medium')],
                            [tg.InlineKeyboardButton('Soul Crushing 🔴', callback_data='quiz_hard')],
                            [tg.InlineKeyboardButton('Main Menu', callback_data='quiz_menu'), tg.InlineKeyboardButton('Give Up 🙉', callback_data='main_cancel')]
                        ])

            
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

        elif query.data == 'main_text':
            query.message.edit_reply_markup(self.text_menu)

        elif query.data == 'main_fun':
            query.message.edit_reply_markup(self.fun_menu)

        elif query.data == 'main_random':
            query.message.edit_reply_markup(self.random_menu)

        elif query.data == 'main_quiz':
            query.message.edit_reply_markup(self.quiz_menu)

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
            media, caption, error = get_meme()

        if query.data == 'img_animal':
            media, caption, error = get_animal()

        if query.data == 'img_asciify':
            user_dp = CHandler().get_dp(query.from_user.id, context)
            media, caption, error = get_asciify(user_dp)    
            user_dp.close()

        if query.data == 'img_human':
            media, caption, error = get_human()

        if query.data == 'img_namo':
            media, caption, error = get_namo()

        if query.data == 'img_hero':
            media, caption, error = get_hero()

        if query.data == 'img_inspire':
            media, caption, error = get_inspire()
            
        if error:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            query.message.edit_media(tg.InputMediaPhoto(media=media, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)
        
        if os.path.exists('static/output.png'):
            media.close()
            os.remove('static/output.png')
        
    def txt_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.text_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = get_caption(query.data)
        
        if error:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)
        
    def fun_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.fun_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = get_fun_caption(query.data)
        
        if error:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)
        
    def rdm_actions(self, update, context):
        query = update.callback_query
        reply_markup = self.random_menu
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="Working on it...", show_alert=False)

        caption, error = get_rdm_caption(query.data)
        
        if error:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=constants.ERROR_TXT, parse_mode="Markdown"), reply_markup=reply_markup)
        else:
            query.message.edit_media(tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=caption, parse_mode="Markdown"), reply_markup=reply_markup)
        
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
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")
            
        if query.data == 'exe_pwd':
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            text = "*Here's your password. Click to copy.*\n\n`{}`".format(pwd)
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")
            
        if query.data == 'exe_alias':
            alias = "-".join([random.choice(constants.ADJECTIVES), random.choice(constants.NOUNS)])
            text = "*Here's your alias. Click to copy*.\n\n`{}`".format(alias)
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        if query.data == 'exe_mod':
            media = tg.InputMediaDocument(media=constants.SPOTIFY_MOD, caption=constants.SPOTIFY_CAP, parse_mode="Markdown")
        
        if query.data == 'exe_web':
            text = constants.USEFUL_WEBSITE_MSG
            media = tg.InputMediaPhoto(media=urls.NICOLE_DP_URL, caption=text, parse_mode="Markdown")

        query.message.edit_media(media=media, reply_markup=reply_markup)

    def respond(self, update, context):
        if update.message and update.message.chat.type == 'private':
            update.message.reply_text(self.kernel.respond(update.message.text))
                
        if update.edited_message and update.edited_message.chat.type == 'private':
            update.message.reply_text(self.kernel.respond(update.message.text))

        elif update.message.reply_to_message:
            if update.message.reply_to_message.from_user.username == 'a_ignorant_mortal_bot':
                update.message.reply_text(self.kernel.respond(update.message.text))
            else:
                pass #In groups, Nicole will reply if someone replies to its message

    def error(self, update, context):
        self.logger.warning('Update that caused the error, \n\n"%s" \n\nThe Error "%s"', update, context.error)
        if update.callback_query.id != None:
            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=constants.ERROR_TXT, show_alert=True)

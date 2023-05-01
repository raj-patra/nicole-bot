import logging
import os
import random

import requests
import telegram as tg
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes

from helpers import constants, urls

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


class CHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.help_menu = tg.InlineKeyboardMarkup([
            [tg.InlineKeyboardButton("slap", callback_data="help_slap"),tg.InlineKeyboardButton("shit", callback_data="help_shit"),tg.InlineKeyboardButton("haha", callback_data="help_haha")],
            [tg.InlineKeyboardButton("doge", callback_data="help_doge"),tg.InlineKeyboardButton("bruh", callback_data="help_bruh"),tg.InlineKeyboardButton("weak", callback_data="help_weak")],
            [tg.InlineKeyboardButton("gay", callback_data="help_gay"),tg.InlineKeyboardButton("lit", callback_data="help_lit"),tg.InlineKeyboardButton("oof", callback_data="help_oof")],
        ])

    def __str__(self):
        return "CHandler helps handle all commands of Nicole."

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        caption = "Here's a list of commands available for Nicole right now. \n\nClick on any of the buttons below to see how to properly invoke these commands."
        await update.message.reply_photo(photo=urls.NICOLE_DP_URL, caption=caption, reply_markup=self.help_menu)

    async def help_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        cmd = query.data.split("_")[1]

        await query.message.edit_media(tg.InputMediaPhoto(media=constants.meme_handler[cmd]["help_pic"], caption=constants.meme_handler[cmd]["help_text"]), reply_markup=self.help_menu)

    async def dev(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_markup = tg.InlineKeyboardMarkup([
            [tg.InlineKeyboardButton("LinkTree", url=urls.DEV_LINKTREE_URL), tg.InlineKeyboardButton("GitHub", url=urls.DEV_GITHUB_URL)],
            [tg.InlineKeyboardButton("Portfolio", url=urls.DEV_PORTFOLIO_URL)]
        ])

        await update.message.reply_photo(photo=urls.DEV_QR_URL, caption=constants.DEV_TXT, parse_mode="Markdown", reply_markup=reply_markup)

    async def roast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            if update.message.reply_to_message.from_user.username == "a_ignorant_mortal_bot":
                await update.message.reply_text("Classic... You thought you could fool me into roasting myself? :) \n\nNot gonna happen.")
            else:
                try:
                    target = "@"+update.message.reply_to_message.from_user.username
                except TypeError:
                    target = update.message.reply_to_message.from_user.first_name

                with open("static/insult.txt") as f:
                    insult = random.choice(f.readlines())
                    if "##name##" in insult:
                        insult = insult.replace("##name##", target)
                    else:
                        insult = target +", "+ insult

                    await update.message.reply_text(insult, quote=False)

        except AttributeError:
            await update.message.reply_text("Reply a group member\"s message with the command 🙏🏻")

    async def get_dp(self, user_id, context):
        try:
            profile = random.choice(await context.bot.getUserProfilePhotos(user_id=user_id)["photos"])
            file_path = await context.bot.getFile(profile[0]["file_id"])["file_path"]
            dp = Image.open(requests.get(file_path, stream=True).raw)
        except IndexError:
            dp = Image.open("static/dp/default.jpg")

        return dp

    async def meme(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cmd = update.message.text.split("@")[0].split("/")[-1]
        meme = Image.open(constants.meme_handler[cmd]["path"])

        if update.message.reply_to_message:
            try:
                target_id = update.message.reply_to_message.from_user.id
                target_msg = update.message.reply_to_message.message_id
                target_name = "@"+update.message.reply_to_message.from_user.username
            except TypeError:
                target_name = update.message.reply_to_message.from_user.first_name

            user_id = update.message.from_user.id
            user_dp = self.get_dp(user_id, context).resize(constants.meme_handler[cmd]["user_resize"])
            meme.paste(user_dp, constants.meme_handler[cmd]["user_pos"])

            if cmd not in ["bruh", "weak", "gay", "oof", "holup"]:
                target_dp = self.get_dp(target_id, context).resize(constants.meme_handler[cmd]["target_resize"])
                meme.paste(target_dp, constants.meme_handler[cmd]["target_pos"])

            meme.save("static/output.png", "PNG")
            await update.message.reply_photo(open("static/output.png", "rb"), caption=target_name+" "+constants.meme_handler[cmd]["caption"], reply_to_message_id=target_msg)

            user_dp.close()
            os.remove("static/output.png")

        else:
            await update.message.reply_text("Reply a group member\"s message with the command 🙏🏻")

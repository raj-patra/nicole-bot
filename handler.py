import logging, os, requests, random
import telegram as tg

from PIL import Image
from helpers.urls import *
from helpers.constants import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class CMDHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.help_menu = tg.InlineKeyboardMarkup([
            [tg.InlineKeyboardButton('slap', callback_data='help_slap'),tg.InlineKeyboardButton('shit', callback_data='help_shit'),tg.InlineKeyboardButton('haha', callback_data='help_haha')],
            [tg.InlineKeyboardButton('doge', callback_data='help_doge'),tg.InlineKeyboardButton('bruh', callback_data='help_bruh'),tg.InlineKeyboardButton('weak', callback_data='help_weak')]
        ])
    
    def __str__(self):
        return "CMDHandler helps handle all commands of Nicole."

    def help(self, update, context):
        caption = "Here's a list of commands available for Nicole right now. \n\nClick on any of the buttons below to see how to properly invoke these commands."
        update.message.reply_photo(photo=NICOLE_DP_URL, caption=caption, reply_markup=self.help_menu)
    
    def help_actions(self, update, context):
        query = update.callback_query
        cmd = query.data.split('_')[1]

        query.message.edit_media(tg.InputMediaPhoto(media=meme_handler[cmd]["help_pic"], caption=meme_handler[cmd]["help_text"]), reply_markup=self.help_menu)

    def dev(self, update, context):
        info = "Made with Py3 and AIML. \nFor any queries contact, [a_ignorant_mortal](https://t.me/a_ignorant_mortal) \n\nMore about the dev: [Linktree](https://linktr.ee/ign_mortal)"
        update.message.reply_text(info, parse_mode="Markdown")

    def roast(self, update, context):
        # insult = requests.get(INSULT_URL).json()['insult']
        try:
            if update.message.reply_to_message.from_user.username == 'a_ignorant_mortal_bot':
                update.message.reply_text("Classic... You thought you could fool me into roasting myself? :) \n\nNot gonna happen.")
            else:
                try:
                    target = '@'+update.message.reply_to_message.from_user.username
                except TypeError:
                    target = update.message.reply_to_message.from_user.first_name

                with open('static/insult.txt') as f:
                    insult = random.choice(f.readlines())
                    if '##name##' in insult:
                        insult = insult.replace("##name##", target)
                    else:
                        insult = target +', '+ insult
                    update.message.reply_text(insult, quote=False)
                    
        except AttributeError:
            update.message.reply_text('And whom should I roast? -_- \nReply a user in a group pls _/\_')

    def get_dp(self, user_id, context):
        try:
            profile = random.choice(context.bot.getUserProfilePhotos(user_id=user_id)['photos'])
            file_path = context.bot.getFile(profile[0]['file_id'])['file_path']
            dp = Image.open(requests.get(file_path, stream=True).raw)
        except IndexError:
            dp = Image.open("static/dp/default.jpg")

        return dp

    def meme(self, update, context):
        cmd = update.message.text[1:5]
        meme = Image.open(meme_handler[cmd]["path"])

        if update.message.reply_to_message:
            try:
                target_id = update.message.reply_to_message.from_user.id
                target_name = '@'+update.message.reply_to_message.from_user.username
            except TypeError:
                target_name = update.message.reply_to_message.from_user.first_name  

            user_id = update.message.from_user.id
            user_dp = self.get_dp(user_id, context).resize(meme_handler[cmd]["user_resize"])
            meme.paste(user_dp, meme_handler[cmd]["user_pos"])

            if cmd not in ['bruh', 'weak']:
                target_dp = self.get_dp(target_id, context).resize(meme_handler[cmd]["target_resize"])
                meme.paste(target_dp, meme_handler[cmd]["target_pos"])
            
            meme.save('static/output.png', 'PNG')
            update.message.reply_photo(open('static/output.png', 'rb'), caption=target_name+' '+meme_handler[cmd]["caption"])
            os.remove('static/output.png')

        else:
            update.message.reply_text('And whom should I slap? -_- \nReply a user in a group pls _/\_')
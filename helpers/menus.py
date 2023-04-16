"""Contains all the inline keyboard menus for the bot"""

import telegram as tg

MENUS = {
    "main_quiz": tg.InlineKeyboardButton('Quizzeria 💡', callback_data="main_quiz"),
    "main_visuals": tg.InlineKeyboardButton('Visuals 🌆', callback_data="main_image"),
    "main_quotify": tg.InlineKeyboardButton('Quotify 📝', callback_data="main_quote"),
    "main_service": tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_service"),
    "main_trivia": tg.InlineKeyboardButton('Trivia 🔀', callback_data="main_trivia"),
    "main_recreation": tg.InlineKeyboardButton('Recreation 🥳', callback_data="main_joke"),
    
    "visuals_animal": tg.InlineKeyboardButton('Nat Geo 🌏', callback_data='image_animal'),
    "visuals_hero": tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='image_hero'),
    "visuals_inspire": tg.InlineKeyboardButton('Inspire Robot 🎇', callback_data='image_inspire'),
    
    "back": tg.InlineKeyboardButton('◀ Back', callback_data='back'),
    "cancel": tg.InlineKeyboardButton('Cancel ❌', callback_data='main_cancel'),
}

DEPR_MENUS = {
    "visuals_meme": tg.InlineKeyboardButton('Reddit Guild 🤙', callback_data='image_meme'),
    "visuals_namo": tg.InlineKeyboardButton('NaMo NaMo 🙏🏻', callback_data='image_namo'),
    "visuals_asciffy": tg.InlineKeyboardButton('Asciify 🧑', callback_data='image_asciify'),
    "visuals_human": tg.InlineKeyboardButton('Imaginary Person 👁👄👁', callback_data='image_human'),
}
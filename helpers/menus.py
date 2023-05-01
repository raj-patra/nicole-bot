"""Contains all the inline keyboard menus for the bot"""

import telegram as tg

MENUS = {
    "main_quiz": tg.InlineKeyboardButton('Quizzeria 💡', callback_data="main_quiz"),
    "main_visuals": tg.InlineKeyboardButton('Visuals 🌆', callback_data="main_image"),
    "main_quotify": tg.InlineKeyboardButton('Quotify 📝', callback_data="main_quote"),
    "main_service": tg.InlineKeyboardButton('Services & Utilities 🛠', callback_data="main_service"),
    "main_trivia": tg.InlineKeyboardButton('Trivia 🔀', callback_data="main_trivia"),
    "main_recreation": tg.InlineKeyboardButton('Recreation 🥳', callback_data="main_joke"),

    "quiz_random": tg.InlineKeyboardButton('Let Fate Decide 🔀', callback_data='quiz_random'),
    "quiz_easy": tg.InlineKeyboardButton('Beginner 🟢', callback_data='quiz_easy'),
    "quiz_medium": tg.InlineKeyboardButton('No Mercy 🟡', callback_data='quiz_medium'),
    "quiz_hard": tg.InlineKeyboardButton('Soul Crushing 🔴', callback_data='quiz_hard'),
    "quiz_menu": tg.InlineKeyboardButton('Main Menu', callback_data='quiz_menu'),

    "visuals_animal": tg.InlineKeyboardButton('Nat Geo 🌏', callback_data='image_animal'),
    "visuals_hero": tg.InlineKeyboardButton('Summon a Superhero 🦸‍♂️🦸‍♀️', callback_data='image_hero'),
    "visuals_inspire": tg.InlineKeyboardButton('Inspire Robot 🎇', callback_data='image_inspire'),

    "quotes_poem": tg.InlineKeyboardButton("Poemist ✍️", callback_data='quotes_poem'),
    "quotes_popular": tg.InlineKeyboardButton('Random Quotes 💯', callback_data='quote_popular'),
    "quotes_stoic": tg.InlineKeyboardButton('Stoicism 🦾', callback_data='quote_stoic'),
    "quotes_advice": tg.InlineKeyboardButton('Free Advice 🆓', callback_data='quote_advice'),
    "quotes_affirmation": tg.InlineKeyboardButton('Build Morale 😇', callback_data='quote_affirmation'),
    "quotes_inspire": tg.InlineKeyboardButton('Stay Inspired 🐱‍👤', callback_data='quote_inspire'),
    "quotes_anime": tg.InlineKeyboardButton('Anime Chan 🗯', callback_data='quote_anime'),

    "recreation_dad": tg.InlineKeyboardButton('Dad Energy 🧔', callback_data='joke_dad'),
    "recreation_roast": tg.InlineKeyboardButton('Roast Me 🔥', callback_data='joke_roast'),
    "recreation_kanye": tg.InlineKeyboardButton('Kanye West 🧭', callback_data='joke_kanye'),
    "recreation_trump": tg.InlineKeyboardButton('Donald Trump 🎺', callback_data='joke_trump'),
    "recreation_chuck": tg.InlineKeyboardButton('Chuck Norris 😈', callback_data='joke_chuck'),

    "trivia_facts": tg.InlineKeyboardButton('Useless Trivia 🤯', callback_data='trivia_facts'),
    "trivia_cats": tg.InlineKeyboardButton('Cat Trivia 😺', callback_data='trivia_cats'),
    "trivia_dogs": tg.InlineKeyboardButton('Dog Trivia 🐶', callback_data='trivia_dogs'),
    "trivia_number": tg.InlineKeyboardButton('Number Trivia 🔢', callback_data='trivia_number'),
    "trivia_date": tg.InlineKeyboardButton('Date Trivia 📆', callback_data='trivia_date'),
    "trivia_year": tg.InlineKeyboardButton('Year Trivia 📅', callback_data='trivia_year'),
    "trivia_math": tg.InlineKeyboardButton('Math Trivia ➕', callback_data='trivia_math'),

    "service_bored": tg.InlineKeyboardButton('Bored Button 🥱', callback_data='service_bored'),
    "service_web": tg.InlineKeyboardButton('Useful Websites </>', callback_data='service_web'),
    "service_mod": tg.InlineKeyboardButton('Spotify Premium Mod 💚', callback_data='service_mod'),
    "service_pwd": tg.InlineKeyboardButton('Password Generator', callback_data='service_pwd'),
    "service_alias": tg.InlineKeyboardButton('Alias Generator', callback_data='service_alias'),

    "back": tg.InlineKeyboardButton('◀ Back', callback_data='misc_back'),
    "cancel": tg.InlineKeyboardButton('Cancel ❌', callback_data='misc_cancel'),
}

MAIN_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["main_quiz"]],
        [MENUS["main_visuals"], MENUS["main_quotify"]],
        [MENUS["main_service"]],
        [MENUS["main_trivia"], MENUS["main_recreation"]],
        [MENUS["cancel"]],
    ]
)
QUIZ_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["quiz_random"]],
        [MENUS["quiz_easy"], MENUS["quiz_medium"]],
        [MENUS["quiz_hard"]],
        [MENUS["quiz_menu"], MENUS["cancel"]],
    ]
)
VISUALS_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["visuals_animal"], MENUS["visuals_inspire"]],
        [MENUS["visuals_hero"]],
        [MENUS["back"], MENUS["cancel"]],
    ]
)
QUOTES_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["quotes_poem"]],
        [MENUS["quotes_popular"], MENUS["quotes_stoic"]],
        [MENUS["quotes_advice"]],
        [MENUS["quotes_affirmation"], MENUS["quotes_inspire"]],
        [MENUS["quotes_anime"]],
        [MENUS["back"], MENUS["cancel"]],
    ]
)
RECREATION_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["recreation_dad"],MENUS["recreation_roast"]],
        [MENUS["recreation_kanye"]],
        [MENUS["recreation_trump"],MENUS["recreation_chuck"]],
        [MENUS["back"], MENUS["cancel"]],
    ]
)
TRIVIA_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["trivia_facts"]],
        [MENUS["trivia_cats"], MENUS["trivia_dogs"]],
        [MENUS["trivia_number"]],
        [MENUS["trivia_date"], MENUS["trivia_year"]],
        [MENUS["trivia_math"]],
        [MENUS["back"], MENUS["cancel"]],
    ]
)
SERVICE_MENU = tg.InlineKeyboardMarkup(
    [
        [MENUS["service_bored"],MENUS["service_web"]],
        [MENUS["service_mod"]],
        [MENUS["service_pwd"],MENUS["service_alias"]],
        [MENUS["back"], MENUS["cancel"]],
    ]
)

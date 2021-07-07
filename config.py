import os
# ----------------------------------------------------------------------------------

PORT = int(os.environ.get('PORT'))
APP_NAME = os.environ.get('APP_NAME')
URL = 'https://{}.herokuapp.com/'.format(APP_NAME)
TOKEN = str(os.environ['BOT_TOKEN'])

# ----------------------------------------------------------------------------------

DOG_PIC_URL = "https://dog.ceo/api/breeds/image/random"
DOG_CAP_URL = "https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1"
CAT_PIC_URL = "https://thatcopy.pw/catapi/rest/"
CAT_CAP_URL = "https://cat-fact.herokuapp.com/facts/random"

RANDOM_HUMAN_URL = "https://thispersondoesnotexist.com/image"
MEME_URL = "https://meme-api.herokuapp.com/gimme"
NAMO_URL = "https://namo-memes.herokuapp.com/memes/1"
HERO_BASE_URL = "https://akabab.github.io/superhero-api/api/id/"
HERO_CDN_URL = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/id/"

# ----------------------------------------------------------------------------------

QUOTE_URL = "https://api.quotable.io/random"
INSULT_URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
FACTS_URL = "https://uselessfacts.jsph.pl//random.json?language=en"
POEMS_URL = "https://www.poemist.com/api/v1/randompoems"
KANYE_URL = "https://api.kanye.rest/"
TRUMP_URL = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
DAILY_URL = "https://www.boredapi.com/api/activity/"

# ----------------------------------------------------------------------------------

RANDOM_WEBSITE_URL = "https://www.boredbutton.com/random"
AGE_URL = "https://api.agify.io/"

# ----------------------------------------------------------------------------------

USEFUL_WEBSITE_URL = """
Here's a list of websites that might help you surf the web better. :)

*Services*
[LinkTree](https://linktr.ee/) - Assemble all your links
[Temp Mail](https://temp-mail.org/en/) - Disposable temporary email
[Pure Speed](http://openspeedtest.com/?ref=OST-Results) - Internet spped test
[Read Something Great](https://www.readsomethinggreat.com/) - Read an interesting article

*Utilities*
[123apps](https://123apps.com/) - Free web apps
[Youtube to MP3](https://y2mate.guru/en4/youtube-to-mp3/) - Extract mp3 from youtube videos
[Cloud Convert](https://cloudconvert.com/) - Convert any file online
[Remove.bg](https://www.remove.bg/upload) - Remove background from image

*Fun*
[Imgflip.com](https://imgflip.com/) - Create and share memes
[Bored Button](https://www.boredbutton.com/random) - Random websites
[Arkadia](http://arkadia.xyz/) - Live wallpaper
[Solar System Map](https://joshworth.com/dev/pixelspace/pixelspace_solarsystem.html) - If the moon were only 1 pixel 
[Wavesync](https://wavesync.herokuapp.com/visualizer) - Spotify Visualizer
"""

# ----------------------------------------------------------------------------------

HERO_MSG = """
*{}*

*Stats :*
    Intelligence - *{}*
    Strength - *{}*
    Speed - *{}*
    Durability - *{}*
    Power - *{}*
    Combat - *{}*

*Appearance :*
    Gender - *{}*
    Species - *{}*
    Height - *{}*
    Weight - *{}*
    Eye color - *{}*
    Hair color - *{}*

*Work* - {}

*Birth Name* - {}
*Alter Egos* - {}
*A.K.A* - {}

*From* - {}
*First Appearance* - {}
*Publisher* - {}

*#{}*
"""

# ----------------------------------------------------------------------------------

HERO_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 20, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53, 56, 57, 58, 60, 61, 62, 63, 66, 68, 69, 70, 71, 72, 73, 75, 76, 78, 79, 80, 81, 82, 83, 84, 87, 88, 92, 93, 95, 96, 97, 98, 99, 100, 
102, 103, 104, 105, 106, 107, 109, 110, 111, 112, 114, 115, 118, 119, 120, 121, 126, 127, 130, 135, 136, 137, 139, 140, 141, 142, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 156, 157, 158, 160, 162, 165, 167, 169, 170, 171, 172, 174, 176, 177, 178, 180, 181, 185, 186, 188, 191, 194, 195, 196, 198, 
200, 201, 202, 203, 204, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 224, 225, 226, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 245, 246, 247, 248, 249, 251, 252, 253, 254, 256, 257, 258, 259, 260, 261, 263, 265, 266, 267, 268, 269, 
270, 271, 273, 274, 275, 277, 278, 280, 284, 285, 286, 287, 288, 289, 294, 296, 297, 298, 299, 300, 303, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 320, 321, 322, 323, 325, 327, 330, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 350, 351, 352, 353, 354, 
355, 356, 357, 358, 360, 361, 364, 365, 367, 369, 370, 371, 372, 373, 374, 375, 376, 379, 380, 381, 382, 383, 384, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 412, 413, 414, 415, 416, 418, 419, 421, 422, 423, 424, 425, 426, 427, 
428, 429, 430, 431, 432, 433, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 448, 449, 450, 451, 452, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 467, 469, 470, 471, 472, 474, 475, 476, 477, 478, 479, 480, 481, 483, 484, 485, 487, 488, 489, 490, 491, 492, 493, 495, 496, 497, 498, 499, 502, 
503, 504, 505, 506, 508, 509, 510, 514, 516, 517, 518, 520, 521, 522, 523, 524, 526, 527, 528, 529, 530, 531, 532, 533, 535, 536, 537, 538, 539, 540, 541, 542, 543, 545, 546, 547, 548, 549, 550, 551, 555, 556, 557, 558, 559, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 
577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 594, 595, 598, 599, 600, 601, 602, 604, 605, 607, 608, 609, 610, 611, 612, 613, 615, 618, 619, 620, 623, 625, 627, 628, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 
651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 664, 665, 666, 667, 668, 670, 671, 672, 676, 677, 678, 679, 680, 681, 685, 686, 687, 688, 689, 690, 692, 693, 696, 697, 699, 701, 702, 703, 705, 706, 707, 708, 709, 711, 713, 714, 716, 717, 718, 719, 720, 722, 723, 724, 726, 727, 728, 729, 730, 731]
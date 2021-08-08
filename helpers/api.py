from . constants import *
from . urls import *
from PIL import Image, ImageDraw

import requests, random, os

def get_meme():
    try:
        response = requests.get(MEME_API).json()
        media = response["url"]
        caption = """*{}* \n\nPosted in [r/{}](www.reddit.com/r/{}) by [u/{}](www.reddit.com/user/{}) \nLink - {}
        
        """.format(response['title'], response['subreddit'], response['subreddit'], response['author'], response['author'], response['postLink'])

        if response['nsfw'] == True:
            caption += "#nsfw"
        if response['spoiler'] == True:
            caption += "#spolier"

        error = None
    except:
        media, caption, error = None, None, True
    finally:
        return media, caption, error

def get_animal():
    try:
        while True:
            choice = random.choice(list(ANIMALS_API.keys()))
            response = requests.get(ANIMALS_API[choice])
            if response.status_code == 200:
                break
            else:
                continue
        json = response.json()
        if choice.endswith("shibe"):
            media = json[0]
        else:
            media = json[choice.split("_")[-1]]

        caption = "Nat Geo approved 🌍"
        error = None
    except:
        media, caption, error = None, None, True
    finally:
        return media, caption, error

def get_asciify(user_dp):
    ASCII_SET = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]

    def resize(image, new_width=100):
        (old_width, old_height) = image.size
        aspect_ratio = old_height / old_width
        new_height = int(aspect_ratio * new_width)
        new_image = image.resize((new_width, new_height))
        return new_image, new_width, new_height

    def PixelToAscii(image, buckets=25):
        pixels = list(image.getdata())
        new_pixels = [ASCII_SET[pixel_value // buckets] for pixel_value in pixels]
        return "".join(new_pixels)

    def saveImage(ascii_str, new_width, new_height):
        image = Image.new(mode="RGB", size=(new_width * 11, new_height * 11), color="white")
        draw = ImageDraw.Draw(image)
        draw.multiline_text((0, 0), ascii_str, fill=(0, 0, 0), align="center", spacing=0)
        image.save("static/output.png")

    def asciify(image):
        image, new_width, new_height = resize(image)
        gray_image = image.convert("L")
        ascii_char_list = PixelToAscii(gray_image)

        len_ascii_list = len(ascii_char_list)
        ascii_str = ""
        ascii_str = "".join([ascii_str + i + i for i in ascii_char_list])

        ascii_str = [
            ascii_str[index : index + 2 * new_width]
            for index in range(0, 2 * len_ascii_list, 2 * new_width)
        ]
        ascii_str = "\n".join(ascii_str)

        saveImage(ascii_str, new_width, new_height)

    asciify(user_dp)
    media = open('static/output.png', 'rb')
    caption = "Pretty wild, isn't it"
    error = False

    return media, caption, error

def get_human():
    try:
        im = Image.open(requests.get(RANDOM_HUMAN_API, stream=True).raw)
        im.save('static/output.png', 'PNG')
        im.close()

        media = open('static/output.png', 'rb')
        caption = "This person does not exist. \nIt was imagined by a GAN (Generative Adversarial Network) \n\nReference - [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com)"
        error = False
    except:
        media, caption, error = None, None, True
    finally:
        return media, caption, error

def get_namo():
    try:
        response = requests.get(NAMO_API)
        if response.status_code == 200:
            media = response.json()[0]["url"]
            caption = "NaMo 🙏🏻"
            error = None
        else:
            media, caption, error = None, None, True
    except:
        media, caption, error = None, None, True
    finally:
        return media, caption, error

def get_hero():
    try:
        while True:
            try:
                response = requests.get(HERO_CDN_API+'{}.json'.format(random.randint(1, 732)))
            except:
                response = requests.get(HERO_BASE_API+'{}.json'.format(random.randint(1, 732)))

            if response.status_code == 200:
                break
            else:
                continue

        response = response.json()
        media = response['images']['lg']
        caption = HERO_MSG.format(response['name'], *response['powerstats'].values(), *response['appearance'].values(), response['work']['occupation'], *response['biography'].values())

        error = False
    except:
        media, caption, error = None, None, True
    finally:
        return media, caption, error


def get_caption(query_data):
    try:
        if query_data == 'txt_quote':
            response = requests.get(QUOTE_API).json()
            caption = "*{}* \n\n- {}".format(response['content'], response['author'])

        if query_data == 'txt_facts':
            response = requests.get(FACTS_API).json()
            caption = "Did you know, \n\n*{}*".format(response['text'])

        if query_data == 'txt_poems':
            response = random.choice(requests.get(POEMS_API).json())
            caption = "*{}* \n\n{} \n\nBy *{}*".format(response['title'], response['content'], response['poet']['name'])

        if query_data == 'txt_kanye':
            response = requests.get(KANYE_API).json()
            caption = "Kanye REST once said, \n\n*{}*".format(response['quote'])

        if query_data == 'txt_trump':
            response = requests.get(TRUMP_API).json()
            caption = "Grumpy Donald once said, \n\n*{}*".format(response['message'])

        if query_data == 'txt_shake':
            response = requests.get(SHAKE_API).json()
            caption = "*{}* \n\n{}\n#{}".format(response['quote']['quote'], response["quote"]["play"], response["quote"]["theme"])

        error = False
    except:
        caption, error = None, True
    finally:
        return caption, error

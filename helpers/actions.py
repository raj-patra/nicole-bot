import random

import requests

from . import constants, urls


class ImageActions:

    def __init__(self) -> None:
        pass # Constructore not required for the class

    def get_animal(self, ):
        try:
            while True:
                choice = random.choice(list(urls.VISUALS_ANIMALS_API.keys()))
                response = requests.get(urls.VISUALS_ANIMALS_API[choice])
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
        except Exception:
            media, caption, error = None, None, True

        return media, caption, error

    def get_hero(self, ):
        try:
            while True:
                try:
                    response = requests.get(urls.VISUALS_HERO_API+"{}.json".format(random.randint(1, 732)))
                except Exception:
                    response = requests.get(urls.VISUALS_HERO_BASE_API+"{}.json".format(random.randint(1, 732)))

                if response.status_code == 200:
                    break
                else:
                    continue

            response = response.json()
            media = response["images"]["lg"]
            caption = constants.HERO_MSG.format(
                response["name"],
                *response["powerstats"].values(),
                *response["appearance"].values(),
                response["work"]["occupation"],
                *response["biography"].values()
            )

            error = False
        except Exception:
            media, caption, error = None, None, True

        return media, caption, error

    def get_inspire(self, ):
        try:
            media = requests.get(urls.VISUALS_INSPIRE_API).text
            caption = "🙏"
            error = None
        except Exception:
            media, caption, error = None, None, True

        return media, caption, error


class TextActions:
    def __init__(self) -> None:
        pass # Constructore not required for the class

    def get_quote(self, query_data):
        try:
            if query_data == "quote_poem":
                response = requests.get(urls.QUOTES_POEM_API).json()
                content = "\n".join(response[0]["lines"])
                caption = "*{}* \n\n{} \n\n- {}".format(response[0]["title"], content, response[0]["author"])

            elif query_data == "quote_popular":
                response = requests.get(urls.QUOTES_POPULAR_API).json()
                caption = "*{}* \n\n- {}".format(response["content"], response["author"])

            elif query_data == "quote_stoic":
                response = requests.get(urls.QUOTES_STOIC_API).json()
                caption = "*{}* \n\n- {}".format(response["quote"], response["author"])

            elif query_data == "quote_advice":
                response = requests.get(urls.QUOTES_ADVICE_API).json()
                caption = "Here's my two cents, \n\n*{}*".format(response["slip"]["advice"])

            elif query_data == "quote_affirmation":
                response = requests.get(urls.QUOTES_AFFIRMATION_API).json()
                caption = "Hey there... Put your chin up,\n\n*{}*".format(response["affirmation"])

            elif query_data == "quote_inspire":
                response = random.choice(requests.get(urls.QUOTES_INSPIRE_API).json())
                caption = "*{}* \n\n- {}".format(response["text"], response["author"])

            elif query_data == "quote_anime":
                response = requests.get(urls.QUOTES_ANIME_API).json()
                caption = "Anime - *{}*\n\n*{}*\n\n- {}".format(response["anime"], response["quote"], response["character"])

            error = False
        except Exception:
            caption, error = None, True

        return caption, error

    def get_trivia(self, query_data):
        try:
            if query_data == "trivia_facts":
                response = requests.get(urls.TRIVIA_FACTS_API).json()
                caption = "Did you know, \n\n*{}*".format(response["text"])

            elif query_data == "trivia_cats":
                response = requests.get(urls.TRIVIA_CATS_API).json()
                caption = "Did you know, \n\n*{}*".format(response["data"][0])

            elif query_data == "trivia_dogs":
                response = requests.get(urls.TRIVIA_DOGS_API).json()
                caption = "Did you know, \n\n*{}*".format(response["data"][0]["attributes"]["body"])

            elif query_data in ["trivia_number", "trivia_date", "trivia_year", "trivia_math"]:
                query_type = query_data.split("_")[1]
                url = urls.TRIVIA_API[query_type]
                response = requests.get(url).text
                caption = "Here's a {type} trivia that you will probably never need. \n\n*{response}*".format(type=query_type, response=response)

            error = False
        except Exception:
            caption, error = None, True

        return caption, error

    def get_recreation(self, query_data):
        try:
            if query_data == "recreation_roast":
                response = requests.get(urls.RECREATION_ROAST_API).text
                caption = "In case nobody ever told you, \n\n*{}*".format(response)

            elif query_data == "recreation_dad":
                response = requests.get(urls.RECREATION_DAD_JOKE_API, headers={"Accept": "application/json"}).json()
                caption = "You know, my dad used to say, \n\n*{}*".format(response["joke"])

            elif query_data == "recreation_corp":
                response = requests.get(urls.RECREATION_CORP_LINGO_API).json()
                caption = "If you ever need big words, just say, \n\n*{}*".format(response["phrase"])

            elif query_data == "recreation_chuck":
                response = requests.get(urls.RECREATION_CHUCK_NORRIS_API).json()
                caption = "The legend has it that, \n\n*{}*".format(response["value"])

            elif query_data == "recreation_trump":
                response = requests.get(urls.RECREATION_TRUMP_API).json()
                caption = "Donald Trump once said, \n\n*{}*".format(response["message"])

            elif query_data == "recreation_kanye":
                response = requests.get(urls.RECREATION_KANYE_API).json()
                caption = "Kanye West once said, \n\n*{}*".format(response["quote"])

            error = False
        except Exception:
            caption, error = None, True

        return caption, error

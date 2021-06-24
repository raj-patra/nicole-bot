import requests
from flask import Flask
from bs4 import BeautifulSoup
from PIL import Image

# doggo = requests.get('https://random.dog/woof.json').json()    
# url = doggo['url']
# print(url)

# rdm = requests.get('https://www.boredbutton.com/random')
# soup = BeautifulSoup(rdm.text, features="html.parser")
# print(soup.find("iframe")["title"], ' : ', soup.find("iframe")["src"])

# im = Image.open(requests.get('https://thiscatdoesnotexist.com', stream=True).raw)
# im.save('pig.png', "PNG")


# print(requests.get("https://evilinsult.com/generate_insult.php?lang={}&type=json".format('en')).json()['insult'])

from app import NicoleBot

nic = NicoleBot()

print(nic.main_menu)
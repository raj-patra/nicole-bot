from config import POEMS_URL
import requests, random
from flask import Flask
from bs4 import BeautifulSoup
from PIL import Image

# im = Image.open("static/slap.jpg")
# im2 = Image.open("static/test1.jpg")
# #Display actual image
# # im.show()

# #Make the new image half the width and half the height of the original image
# resized_im = im2.resize((round(im.size[0]*0.22), round(im.size[1]*0.22)))


# im.paste(resized_im, (210,225))
# # Display the resized imaged
# im.show()
# rdm = requests.get('https://www.boredbutton.com/random')
# soup = BeautifulSoup(rdm.text, features="html.parser")
# print(soup.find("iframe")["title"], ' : ', soup.find("iframe")["src"])

# im = Image.open(requests.get('https://thiscatdoesnotexist.com', stream=True).raw)
# im.save('pig.png', "PNG")

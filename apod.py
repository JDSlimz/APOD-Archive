#!/usr/bin/python

from lxml import html
import requests
from bs4 import BeautifulSoup
import urllib

page = requests.get('https://apod.nasa.gov/apod/astropix.html')
soup = BeautifulSoup(page.text)

apod = "https://apod.nasa.gov/apod" + str( soup.find("img")['src'] )
title =str ( soup.find("b") )
title = title[4:-4]

print(apod)
print(title)
title = title.rstrip()
urllib.urlretrieve("https://apod.nasa.gov/apod" + apod, "PUT YOUR FILEPATH HERE" + title + ".jpg")
apodImg = 'apod.jpg'

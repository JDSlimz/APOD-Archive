#!/usr/bin/python
import os
import sys 
from lxml import html 
import requests 
from bs4 import BeautifulSoup 
import urllib 
import lxml.etree 
import re
import argparse

parser = argparse.ArgumentParser(description="APOD Archive parses all entries in NASAs Astronomy Picture of the Day website archive and downloads the images to a location you specify!")
parser.add_argument('location', type=str, help="The location you would like to store the images.")
parser.add_argument('--log', action='store_true', default=False, help="Enable logging of parsed pages.")
parser.add_argument('--debug', action='store_true', default=False, help="Enable debugging to print to screen.")

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])

#Variables
location = args.location
log = args.log
debug = args.debug
thisLink = 0 
skipped = 0
saved = 0

#Progress Bar
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

#Get requested URL
page = requests.get('https://apod.nasa.gov/apod/archivepix.html') 
soup = BeautifulSoup(page.text, 'lxml') 
body = soup.find('b') 
numberOfLinks = len(body.findAll('a')) 


if not os.path.isdir(location):
    os.makedirs(location)

if log:
    log_file = open(location + '/apodLog.txt', 'w')

#For each link in Soup
for link in body.findAll('a'):
    title = link.contents[0]
    title = title.translate({ord(i):None for i in '<>:"/\\|?*,'})
    title = title.replace('\n','')
    url = link["href"]
    newPage = requests.get("https://apod.nasa.gov/apod/" + url)
    newSoup = BeautifulSoup(newPage.text, 'lxml')

    #If there is an image, download it to "Location"
    if newSoup.find('img'):
        image = newSoup.find('img')["src"]
        #urllib.request.urlretrieve("https://apod.nasa.gov/apod/" + str(image), location + title.rstrip() + ".jpg")

        if log:
            log_file.write("Saved: " + title + '\n')
            saved += 1
        if debug:
            print ("Saved: " + title)

    #If there is not an image, take not and count.
    else:
        if log:
            log_file.write('***' + title + ' no image!***\n')
            skipped += 1
        if debug:
            print ("***" + title + " did not have image!***")
    #progress(thisLink, numberOfLinks, status="Downloading")
    thisLink += 1

if log:
    log_file.write('Downloaded: ' + saved + '\n')
    log_file.write('Skipped: ' + skipped)
    log_file.close()

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
parser.add_argument('-d', '--dir', action='store_true', default=False, help="Setting will prompt you for a desired storage location. Without --dir, APODArchive will store all images and logs in the directory the script is run from.")
parser.add_argument('-l', '--log', action='store_true', default=False, help="Enable logging of parsed pages.")
parser.add_argument('-b', '--debug', action='store_true', default=False, help="Enable debugging to print to screen.")

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])

#Variables
loc = args.dir
if loc:
    location = input("Please specify a storage directory: ") #Ask user for folder
else:
    location = os.path.dirname(os.path.realpath(__file__)) #Get current directory
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


if not os.path.isdir(location): #If the specified directrory does not exist,
    os.makedirs(location) #Make it so!

if log:
    log_file = open(location + '/apodLog.txt', 'w') #Open a new log file.

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

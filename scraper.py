import urllib2
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests

os.environ["LANG"] = "en_US.UTF-8"
#open webpage 3.7
#http = urllib3.PoolManager()
#quote_page = "https://www.terminal5nyc.com/shows/"
#response = requests.get(quote_page)
#soup = BeautifulSoup(response.content, "html.parser")

#open webpage
quote_page = "https%3A//www.terminal5nyc.com/shows/"
html = urlopen(quote_page)
bsObj = BeautifulSoup(html.read());
print(bsObj.h1)

#alt open webpage

soup = BeautifulSoup(response.content, "html.parser")

# click more rows button
#driver = webdriver.Chrome('C:\\Users\\awf54\\Downloads\\chromedriver_win32\\chromedriver.exe')
#driver = webdriver.Firefox('C:\\Users\\awf54\\Documents\\geckodriver\\geckodriver.exe')

driver = webdriver.Firefox('C:\\Users\\awf54\\dev\\concert_mixer\\geckodriver\\geckodriver.exe')
driver = webdriver.Firefox('C:\\Users\\awf54\\Downloads\\geckodriverwin32\\geckodriver.exe')

driver.get(quote_page)
elem = driver.find_elements_by_xpath("//*[@class='button black btShowMore']")

# Grab band, date , price
soup = BeautifulSoup(response.data)
first_bn = soup.find('span', attrs={'itemprop': 'name'}).text
first_bd = soup.find('p', attrs={'class':'list-date'}).text
first_pr = soup.find('$0')

names=soup.findAll('span', attrs={'itemprop': 'name'})





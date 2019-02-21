#note scraper2 is inteded to be run against Python2.7
import urllib2
#from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import common
import time
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import requests
import re

from scraper_util import insert_lists_into_db,get_web_driver

os.environ["LANG"] = "en_US.UTF-8"

#open webpage

# urllib2.urlopen(quote_page)
# page_response = requests.get(quote_page, timeout=5)
# soup = BeautifulSoup(page_response.content, "html.parser")

def get_term5_shows(page):
    loop_try=0
    driver.get(page)
    while loop_try<10:
        elem = driver.find_element_by_css_selector("a.button.black.btshowmore")
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(elem).perform()
        time.sleep(4)
        try :
            elem.click()
        except WebDriverException:
            print('no more pages to load after{}'.format(loop_try))
        loop_try=loop_try+1

    html = driver.page_source
    driver.close()
    return html

# Grab band, date , price
def t5_get_names(html):
    soup = BeautifulSoup(html)
    names=soup.findAll('span', attrs={'itemprop': 'name'})
    names_list=[]
    for i in names:
        names_list.append(i.text)
    return names_list

def t5_get_dates(html):
    soup = BeautifulSoup(html)
    dates=soup.findAll('p', attrs={'class':'list-date'})
    date_list = []
    for i in dates:
        pattern = re.compile('[\S]+ [\d]+, [\d]+')
        match = pattern.search(i.text)
        date_list.append(match.group())
    return date_list

def t5_get_price(html):
    soup = BeautifulSoup(html)
    first_pr = soup.findAll('p')
    price_list = []
    for i in first_pr:
        if 'Advance' in i.text:
            target = i.text.lstrip()
            pattern = re.compile('[\d]+.[\d]+')
            match = pattern.match(target[10:30])
            price_list.append(match.group())
    return price_list


#call functions
driver = get_web_driver()
quote_page = "https://www.terminal5nyc.com/shows/"
term5_html = get_term5_shows(page=quote_page)
names_list = t5_get_names(html=term5_html)
date_list = t5_get_dates(html=term5_html)
price_list = t5_get_price(html=term5_html)

test = insert_lists_into_db(
    namelist = names_list,
    datelist = date_list,
    pricelist = price_list,
    venueid = 1,
    venue = 'terminal5',
    link = quote_page
)




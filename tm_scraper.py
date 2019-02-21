from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium import common
import time
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import os
import requests
import re
from scraper_util import get_config, insert_lists_into_db,get_web_driver


def ticketmaster_get_Event_api(venuename,venueid):
    venuename = 'kings-theatre-tickets-brooklyn'
    venueid = 'KovZpZAJEa6A'
    api_key='hjt7qHDuXiSvfVi1T3ZCccyxszntkJrA' # put in config
    root_url = 'https://app.ticketmaster.com'
    url = 'https://app.ticketmaster.com/discovery/v2'
    type_resp = "/events.json"
    url = url+type_resp
    params = {'apikey': api_key, 'venueId':venueid}
    resp = requests.get(url, params=params)
    ev_resp = resp.json()
    return ev_resp


def venue_to_eventdf(venue_json, venuename):
    events = venue_json['_embedded'][u'events']
    venuename__ = venuename
    venue_df = pd.DataFrame(columns=['venue',
                                     'event_name',
                                     'band_name',
                                     'conc_date',
                                     'conc_price',
                                     'genre',
                                     'subgenre',
                                     'postcode'])

    for i in events:
        if i['dates']['spanMultipleDays'] == False:
            ev_date = i['dates']['start']['localDate']
            name = i['name']
            band_name = i['_embedded']['attractions'][0]['name']
            genre = i['_embedded']['attractions'][0]['classifications'][0]['genre']['name']
            subgenre = i['_embedded']['attractions'][0]['classifications'][0]['subGenre']
            price = i['priceRanges'][0]['min']
            postcode = i['_embedded']['venues'][0]['postalCode']
            evlink = i['url']
            venue_df = venue_df.append({'venue': venuename__,
                                        'event_name': name,
                                        'band_name': band_name,
                                        'conc_date': ev_date,
                                        'conc_price': price,
                                        'genre': genre,
                                        'subgenre': subgenre,
                                        'postcode': postcode}, ignore_index=True)
    return venue_df


def ticketmaster_gethtml(venuename,venueid, driver):
    page = "https://www.ticketmaster.com/{}/venue/{}".format(venuename,venueid)
    driver.get(page)
    html = driver.page_source
    driver.close()
    return html

def tm_get_names(html):
    soup = BeautifulSoup(html)
    names=soup.findAll('span', attrs={'itemprop': 'name'})
    names_list=[]
    for i in names:
        names_list.append(i.text)
    return names_list

def tm_get_dates(html):
    soup = BeautifulSoup(html)
    # dates = soup.findAll('div',attrs={"class":["text--accent"]})
    dates = soup.findAll('div',attrs={"class":["drFkLn"]})
    date_list = []
    for i in dates:
        date_list.append(i.text)
    return date_list

def tm_get_price(html):
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

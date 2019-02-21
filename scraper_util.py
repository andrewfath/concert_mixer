import pandas as pd
import sqlalchemy
from selenium import webdriver
from selenium import common
import mysql.connector
import yaml
# cnx = mysql.connector.connect(user='concert_mixer', password='cmpassword',
#                               host='127.0.0.1',
#                               database='sys')
#
# cnx = mysql.connector.connect(user='root', password='rootpassword',
#                               host='127.0.0.1',
#                               database='sys')

def get_config(yamlname):
    with open("{}.yaml".format(yamlname)) as stream:
        config=yaml.load(stream)
    return config

def insert_lists_into_db(namelist,datelist,pricelist,venueid,venue,link):
    df = pd.DataFrame()
    df['event_name'] = namelist
    df['event_date'] = datelist
    df['price'] = pricelist
    df['venue_id'] = venueid
    df['venue'] = venue
    df['link'] = link
    return df


def get_web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    #options.binary_location = "C:\\Users\\awf54\\Downloads\\chromedriver_win32\\chromedriver.exe"
    #driver = webdriver.Chrome(chrome_options=options)
    # driver.get('http://codepad.org')
    # driver = webdriver.Firefox('C:\\Users\\awf54\\Documents\\geckodriver\\geckodriver.exe')
    driver = webdriver.Chrome(executable_path="C:\\Users\\awf54\\Downloads\\chromedriver_win32_225\\chromedriver.exe")
    return driver

import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



from tm_scraper import get_web_driver, ticketmaster_get_Event_api, \
    ticketmaster_gethtml, tm_get_dates, tm_get_names, tm_get_price,venue_to_eventdf

# conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
# conn = psycopg2.connect(dbname='yourdb', user='dbuser', password='abcd1234', host='server', port='5432', sslmode='require')
conn = psycopg2.connect(host="localhost",database="concert_db", user="postgres", password="pgpassword")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# call api for one event location
event_json = ticketmaster_get_Event_api(
    venuename='kings-theatre-tickets-brooklyn',
    venueid='393357')
eventdf = venue_to_eventdf(venue_json=event_json, venuename='kings-theatre-tickets-brooklyn')

#call api for dictionary of venues
event_dict = {'brooklynbowl':'KovZpZAIetFA',
              'bric summer':'KovZpZAdt7kA',
              'bellhouse':'KovZpZAFJntA',
              'knitting factory':'KovZpZAaFI1A',
              'brooklyn steel':'KovZ917AC-V'}

venue_df = pd.DataFrame(columns=['venue',
                                 'event_name',
                                 'band_name',
                                 'conc_date',
                                 'conc_price',
                                 'genre',
                                 'subgenre',
                                 'postcode'])

for key,value in event_dict.iteritems():
    print (value)
    event_json = ticketmaster_get_Event_api(venuename=key, venueid=value)
    eventdf = venue_to_eventdf(venue_json=event_json, venuename=key)
    venue_df=venue_df.append(eventdf)

# venue_df.groupby('venue').count()

# configf = get_config(yamlname='config')
# config['mariadb ']

# driver = get_web_driver()
# kt_html = ticketmaster_gethtml(
#     venuename='kings-theatre-tickets-brooklyn',
#     venueid = '393357',
#     driver = driver)
# # soup = BeautifulSoup(kt_html)
# tm_get_dates(kt_html)
# tm_get_names(kt_html)








#Find venues:
api_key = 'hjt7qHDuXiSvfVi1T3ZCccyxszntkJrA'
url = 'https://app.ticketmaster.com/discovery/v2'
type_resp = "/venues.json"
url = url + type_resp
params = {'apikey': api_key, 'keyword': 'candy'}
resp = requests.get(url, params=params)
respj = resp.json()
for i in range(len(respj['_embedded']['venues'])):
    print ("{} -{} - {} {}".format(i,
                                 respj['_embedded']['venues'][i]['id'],
                                 respj['_embedded']['venues'][i]['name'],
                                 respj['_embedded']['venues'][i]['url']))
# respj['page] # see num pages
# respj['_embedded']['venues'][0] # example
respj['_embedded']['venues'][0]['id']


venue_json = ticketmaster_get_Event_api(
    venuename='kings-theatre-tickets-brooklyn',
    venueid = '393357')


example0 = venue_json['_embedded'][u'events'][0]

import requests
import pandas as pd
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from scraper_util import get_config

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 100)

"""
Given a user, this script will return...
1) top artists
2) favorite artists
3) artists from playlists
4) artists from user saved tracks
"""

config=get_config('config')
username='jsheynin'
# setup spotify api call
scope = 'user-top-read,user-library-read,user-follow-read,playlist-read-private,playlist-read-collaborative,user-read-recently-played'
username = username
token = util.prompt_for_user_token(username, scope, client_id=config['spotify']['clientid'],
                                   client_secret=config['spotify']['secret'],
                                   redirect_uri=config['spotify']['redirect_uri'])
sp = spotipy.Spotify(auth=token)

def get_follow_artist(sp):
    """
    :param sp: spotify object with user token where scope =
    :return:
    """
    #parse favorite results
    results = sp.current_user_followed_artists()
    artist_df=pd.DataFrame(columns=['spotifyid','name','genres','popularity'])
    for item in results['artists']['items']:
        artist_dict = {'spotifyid':item['id'],
                       'name':item['name'],
                       'genres':''.join(item['genres']),
                       'popularity':item['popularity']}
        artist_df=artist_df.append(artist_dict,ignore_index=True)
    return artist_df

def get_top_artist(sp):
    """
    :param sp: spotify object with user token where scope =
    :return:
    """
    #parse favorite results
    results = sp.current_user_top_artists()
    artist_df=pd.DataFrame(columns=['spotifyid','name','genres','popularity'])
    for item in results['items']:
        artist_dict = {'spotifyid':item['id'],
                       'name':item['name'],
                       'genres':''.join(item['genres']),
                       'popularity':item['popularity']}
        artist_df=artist_df.append(artist_dict,ignore_index=True)
    return artist_df


def get_artist_from_tracks(tracks,sourcename):
    artist_df=pd.DataFrame(columns=['sourcename','spotifyid','name','uri'])
    artistdict={}
    for i, item in enumerate(tracks['items']):
        track = item['track']
        # print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
        #     track['name'])
        if artist_df[artist_df['name'].isin([track['artists'][0]['name']])].empty:
            artistdict['sourcename']=sourcename
            artistdict['name']= track['artists'][0]['name']
            artistdict['spotifyid']= track['artists'][0]['id']
            artistdict['uri']= track['artists'][0]['uri']
            artist_df = artist_df.append(artistdict, ignore_index=True)
        artistdict={}
    return artist_df



def get_playlist_artist(sp):
    """
    :param sp: spotify object with user token where scope =
    :return: ap_dict = a dictionary where each playlist is associated with all it's first artists
    """
    #parse favorite results
    results = sp.current_user_playlists()
    ap_dict={}
    artist_df = pd.DataFrame(columns=['sourcename', 'spotifyid', 'name', 'uri'])
    artist_list=[]
    for playlist in results['items']:
        sub_results = sp.user_playlist(username,playlist['id'],fields="tracks,next")
        tracks = sub_results['tracks']
        artist_df = artist_df.append(get_artist_from_tracks(tracks=tracks,sourcename=playlist['name']))
        while tracks['next']:
            tracks = sp.next(tracks)
            artist_df = artist_df.append(get_artist_from_tracks(tracks=tracks, sourcename=results['items'][1]['name']))
        # artist_list = list(set(artist_list)) #dedupe
    return artist_df

def get_related_artists(sp,id):
    """
    :param sp: spotify object
    :param artistid
    :return: ap_dict = a dictionary where each playlist is associated with all it's first artists
    """
    #parse favorite results
    results = sp.artist_related_artists(artist_id=id)
    artist_df=pd.DataFrame(columns=['spotifyid','name','genres','popularity'])
    for item in results['artists']:
        artist_dict = {'spotifyid':item['id'],
                       'name':item['name'],
                       'genres':''.join(item['genres']),
                       'popularity':item['popularity']}
        artist_df=artist_df.append(artist_dict,ignore_index=True)
    return artist_df


fa = get_follow_artist(sp=sp) #df with cols 'spotifyid', u'name', u'genres', u'popularity'
ta = get_top_artist(sp=sp) #df with cols 'spotifyid', u'name', u'genres', u'popularity'
pdict = get_playlist_artist(sp=sp)
ra = get_related_artists(sp=sp,id=ta['spotifyid'][0]) #df with cols 'spotifyid', u'name', u'genres', u'popularity'

ra = get_related_artists(sp=sp,id='64KEffDW9EtZ1y2vBYgq8T') #df with cols 'spotifyid', u'name', u'genres', u'popularity'



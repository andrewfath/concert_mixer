import requests
import sys
import spotipy
import spotipy.util as util
# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
# export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

token = util.prompt_for_user_token(username='awf541')

sp = spotipy.Spotify(auth=token)
# sp = spotipy.Spotify()
user = sp.user('awf541')


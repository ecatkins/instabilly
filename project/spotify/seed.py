from spotify.models import Song, User, UserSong, Profile
import requests
import spotipy
from spotipy import oauth2
# from spotify.secret import *

def seed():
    x = oauth2.SpotifyOAuth(CLIENTID,CLIENTSECRET,"http://localhost:8000/callback",scope="user-library-read")
    url = x.get_authorize_url()
    tom = requests.get(url)
    print(dir(tom))
    print(tom.url)
    print(tom.raw)
    print(tom.links)
    post_route = "https://accounts.spotify.com/api/token"
    callback = "http://localhost:8000/callback"
    grant_type = "authorization_code"
    pay_load = {"grant_type":grant_type, "code":code, "redirect_uri":callback,"client_id":CLIENTID,"client_secret":CLIENTSECRET}
    r = requests.post(post_route, data=pay_load)
    # print(r.status_code)
    print(r.json())
    token = r.json()['access_token']
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=1)
    print(results)
    count = 0
    while count < results['total']:
      results = sp.current_user_saved_tracks(limit=50,offset=count)
      count += 50
      for x in results['items']:
          print(x['track']['name'])
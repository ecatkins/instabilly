#export SPOTIPY_CLIENT_ID='your-spotify-client-id'
#export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
#export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

from spotify.models import Song, Artist, Genre
from spotify.secret import *
import pyen
import spotipy
import spotipy.util as util




#seeds genres and artists based on existing users
def seed_gen():
    en = pyen.Pyen(APIKEY)
    all_songs = Song.objects.all()
    for song in all_songs:
        artist = Artist.objects.filter(name=song.artist)
        if len(artist) == 0:
            print(song.artist)
            new_artist = Artist(name=song.artist)
            new_artist.save()
            response = en.get('artist/profile', name=song.artist, bucket=['genre'])
            genres = response['artist']['genres']
            for genre in genres:
                existing = Genre.objects.filter(name=genre['name'])
                if len(existing) == 0:
                    genre_object = Genre(name=genre['name'])
                    genre_object.save()
                    print(genre)
                else:
                    genre_object = existing[0]
                new_artist.genres.add(genre_object)
            new_artist.save()

#seed random users
# My-username:
# 2rkfKrh8R3muuHrkENu30P
eddy_username = "11800860"
def seed_random_users():
    token = util.prompt_for_user_token(eddy_username)
    sp = spotipy.Spotify(auth=token)
    response = sp.featured_playlists()

    while response:
        playlists = response['playlists']
        for i, item in enumerate(playlists['items']):
            print(playlists['offset'] + i, item['name'])

        if playlists['next']:
            response = sp.next(playlists)
        else:
            response = None

    new_search = sp.search(q="Totally Stress Free",type="playlist")
    print(new_search[0])






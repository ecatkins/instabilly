from spotify.models import Song, Artist, Genre
from spotify.secret import *
import pyen
import spotipy
import spotipy.util as util
import pdb

def seed_genre(artist_name):
    en = pyen.Pyen(APIKEY)
    new_artist = Artist(name=artist_name)
    new_artist.save()
    try:
        response = en.get('artist/profile', name=artist_name, bucket=['genre'])
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
    except:
        pass
    return new_artist









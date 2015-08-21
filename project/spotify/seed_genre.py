from spotify.models import Song, Artist, Genre
from spotify.secret import *
import pyen
import spotipy
import spotipy.util as util

#seeds genres and artists based on existing users
# def seed_gen():
#     en = pyen.Pyen(APIKEY)
#     all_songs = Song.objects.all()
#     for song in all_songs:
#         artist = Artist.objects.filter(name=song.artist)
#         if len(artist) == 0:
#             try:
#                 print(song.artist)
#                 new_artist = Artist(name=song.artist)
#                 new_artist.save()
#                 response = en.get('artist/profile', name=song.artist, bucket=['genre'])
#                 genres = response['artist']['genres']
#                 for genre in genres:
#                     existing = Genre.objects.filter(name=genre['name'])
#                     if len(existing) == 0:
#                         genre_object = Genre(name=genre['name'])
#                         genre_object.save()
#                         print(genre)
#                     else:
#                         genre_object = existing[0]
#                     new_artist.genres.add(genre_object)
#                 new_artist.save()
#             except:
#                 continue


def seed(artist_name):
    en = pyen.Pyen(APIKEY)
    new_artist = Artist(name=artist_name)
    new_artist.save()
    try:
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
    except:
        continue
    return new_artist









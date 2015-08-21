from spotify.models import Song, Artist

def migrate_artists():
	all_songs = Song.objects.all()
	for song in all_songs:
		artist_name = song.artist
		artist_object = Artist.objects.get(name=artist_name)
		song.artists = artist_object
		song.save()
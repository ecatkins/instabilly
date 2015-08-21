from spotify.models import User, UserSong, Song, Genre, Artist

test_user = User.objects.get(username="ecatkins")

# def get_all_genres():
	

def genre_user_array(user):
	all_genre_names = [x.name for x in Genre.objects.all()]
	print(all_genre_names)
	genre_array = [0]*len(all_genre_names)
	user_songs = UserSong.objects.filter(user=user)
	number_songs = len(user_songs)
	all_artists = Artist.objects.all()
	for song in user_songs:
		for artist in all_artists:
			if song.song.artist == artist.name:
				genres = artist.genres.all()
				for genre in genres:
					index = all_genre_names.index(genre.name)
					genre_array[index] += 1
	genre_percent_array = [x/number_songs for x in genre_array]
	print(genre_array)
	print(genre_percent_array)





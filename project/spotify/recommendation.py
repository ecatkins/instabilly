from spotify.models import User, UserSong, Song, Genre, Artist
from sklearn.neighbors import KNeighborsClassifier
import random


test_user = User.objects.get(username="ecatkins")


def genre_user_array(user):
	all_genre_names = [x.name for x in Genre.objects.all()]
	# print(all_genre_names)
	genre_array = [0]*len(all_genre_names)
	user_songs = UserSong.objects.filter(user=user)
	number_songs = max(1,len(user_songs))
	all_artists = Artist.objects.all()
	for song in user_songs:
		artist = song.song.artists
		genres = artist.genres.all()
		for genre in genres:
			index = all_genre_names.index(genre.name)
			genre_array[index] += 1
	genre_percent_array = [x/number_songs for x in genre_array]
	# print(genre_array)
	return (genre_percent_array)


def similar_users(user,neighbors):
	name_array = []
	x_array = []
	all_users = User.objects.exclude(pk=user.pk)
	# all_users = User.objects.all()
	for user in all_users:
		name_array.append(user.username)
		print(user.username)
		genre_array = genre_user_array(user)
		x_array.append(genre_array)
	y_array = [random.random() for x in range(len(x_array))]
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(x_array, y_array)
	print(name_array)
	test = genre_user_array(test_user)
	result = neigh.kneighbors((test),neighbors)
	similar_users = [name_array[result[1][0][x]] for x in range(neighbors)]
	return similar_users

def create_playlist(user,neighbors,number_songs):
	similar = similar_users(user,neighbors)
	playlist = []
	count = 0 
	while count < number_songs:
		for user in similar:
			user_object = User.objects.get(username=user)
			user_songs = UserSong.objects.filter(user=user_object)
			random_song = user_songs[random.randrange(0,len(user_songs))]
			playlist.append(random_song.song.track_name)
			count += 1
	print(playlist)















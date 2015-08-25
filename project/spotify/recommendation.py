from spotify.models import User, UserSong, Song, Genre, Artist, ArtistRecommendation
from sklearn.neighbors import KNeighborsClassifier
import random
import datetime
import pdb


# test_user = User.objects.get(username="ecatkins")
# test_user2 = User.objects.get(username="Wilson")
# test_user3 = User.objects.get(username="adamrj")


def genre_user_array(user):
	all_genre_names = [x.name for x in Genre.objects.all()]
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
	return (genre_percent_array)


def similar_users(user,neighbors):
	''' Pass: the active user object and the number of neighbors to calculate
		Returns: An array of similar users, containing the username and the distance to that user on the genre-dimensional plot
	 '''
	name_array = []
	x_array = []
	all_users = User.objects.exclude(pk=user.pk)
	# all_users = User.objects.all()
	for other_user in all_users:
		if len(UserSong.objects.filter(user=other_user)) != 0:
			name_array.append(other_user.username)
			genre_array = genre_user_array(other_user)
			x_array.append(genre_array)
	y_array = [random.random() for x in range(len(x_array))]
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(x_array, y_array)
	user_genres = genre_user_array(user)
	result = neigh.kneighbors((user_genres),neighbors)
	similar_users = [[name_array[result[1][0][x]],result[0][0][x]] for x in range(neighbors)]
	return similar_users

def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i


def get_user_song_array(similar):
	user_songs_array = []
	for user in similar:
		user_object = User.objects.get(username=user[0])
		user_songs = UserSong.objects.filter(user=user_object)
		user_songs_array.append(user_songs)
	return user_songs_array

def return_tracks_recency_bias(user_songs_array,number_songs,recency_effect):
	''' Pass: an array with user songs of n users
		Return: An array equal to the length of the playlist each containing a sub array with a song selected from each with neighbor with a bias
			towards recent songs
	'''
	return_array = []
	for x in range(number_songs):
		return_array.append([])
	for user in user_songs_array:
		age = [(datetime.datetime.now().date() - song.uploaded_at).days for song in user]
		weighted_age = [1/(0.0005*(x+20)) for x in age]
		average = sum(weighted_age) / len(weighted_age)
		#Adjusts for effect
		weighted_age = [x - (x-average)*(1-recency_effect) for x in weighted_age]
		for song in range(number_songs):
			choice = weighted_choice(weighted_age)
			return_array[song].append(user[choice])
	return return_array

	
def duplicate_artist(playlist,user_song):
	for song in playlist:
		if song.song.artists.name == user_song.song.artists.name:
			return True
	return False



def create_playlist(user,neighbors,number_songs,recency_effect,rating_effect,duplicate_artist_effect,existing_playlist_effect):
	'''Pass: the active user, number of neighbors to inform recommendation and
	 number of songs desired in playlist
	 Returns: Array of song objects '''
	print("0")
	similar = similar_users(user,neighbors)
	playlist = []
	user_songs = get_user_song_array(similar)
	print("1")
	song_choice = return_tracks_recency_bias(user_songs,number_songs,recency_effect)


	### Weighting factor 1, similarity to current user
	print("2")
	distances = [1/x[1] for x in similar]
	print("Distances{}".format(distances))
	for song_number in song_choice:
		print("3")
		recommendation_array = []
		replication_array = []
		existing_playlist_array = []
		for user_song in song_number:
			print("4")
			### Weighting factor 2, user previous recommendations of artist
			recommendation = ArtistRecommendation.objects.filter(user=user,artist=user_song.song.artists)
			print("5")
			if len(recommendation) == 1:
				score = recommendation.score
			else:
				score = 0.5
			print("6")
			#Adjusts for effect
			score = score - (score-0.5)*(1-rating_effect)
			recommendation_array.append(score)
			print("7")
			### Weighting factor 3, no replicated artists in playlist
			if duplicate_artist(playlist,user_song) == True:
				replication_array.append(1-(duplicate_artist_effect))
			else:
				replication_array.append(1)
			print("8")
			### Weighting factor 4, already in user playlist
			existing = UserSong.objects.filter(user=user,song = user_song.song)
			if len(existing) == 1:
				existing_playlist_array.append(1-existing_playlist_effect)
			else:
				existing_playlist_array.append(1)
			print("9")
		#Multiply arrays
		final_weighting_array = []
		for x in range(len(distances)):
			final_weighting  = distances[x] * recommendation_array[x] * replication_array[x] * existing_playlist_array[x]
			final_weighting_array.append(final_weighting)
		# Needs fixing to ensure that playlist is of conistent length
		if sum(final_weighting_array) == 0:
			continue
		### select song
		choice = weighted_choice(final_weighting_array)
		playlist.append(song_number[choice])
		print("10")
	

	return playlist











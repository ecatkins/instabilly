from spotify.models import User, UserSong, Song, Genre, Artist, ArtistRating, UserGenre, FollowList
from sklearn.neighbors import KNeighborsClassifier
import random
import datetime
import pdb

def test_get_usergenre_for_these_users(search=None):
	if not search:
		UserGenre.objects.values('id','proportion', 'user_id', 'genre_id')

def get_genre_arrays(user):

	all_user_genres = UserGenre.objects.filter(proportion__gt = 0).values('id','proportion', 'user_id', 'genre_id').order_by('user_id')
	genre_count = Genre.objects.count()
	genres = Genre.objects.all()
	genre_count_array = [i for i in range(genre_count)]
	all_user_genres_pks = [j.pk for j in genres]
	zipped_genre_dictionary = dict(zip(all_user_genres_pks,genre_count_array))
	counter = -1
	current_user_id = 0
	id_array = []
	x_array = []
	user_array = []
	for row in all_user_genres:
		if row['user_id'] != current_user_id and row['user_id'] != user.pk:
			id_array.append(row['user_id'])
			x_array.append([0] * genre_count)
			counter += 1
			current_user_id = row['user_id']
			array = x_array[counter]
		elif row['user_id'] == user.pk and not user_array:
			user_array = [0] * genre_count
			array = user_array
		array[zipped_genre_dictionary[row['genre_id']]] = row['proportion']
	return id_array, x_array, user_array



def similar_users(user,neighbors):
	''' Pass: the active user object and the number of neighbors to calculate
		Returns: An array of similar users, containing the username and the distance to that user on the genre-dimensional plot
	 '''
	# pdb.set_trace()
	id_array, x_array,user_array = get_genre_arrays(user)
	y_array = [random.random() for x in range(len(x_array))]
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(x_array, y_array)
	result = neigh.kneighbors((user_array),neighbors)
	similar_users = [[id_array[result[1][0][x]],result[0][0][x]] for x in range(neighbors)]
	return similar_users

def follow_users(similar,follow_number,follow_list):
	similar_distances_average = sum([x[1] for x in similar]) / len(similar)
	follow_users = []
	for x in range(follow_number):
		random_follow_id = random.choice(follow_list).pk
		follow_users.append([random_follow_id,similar_distances_average])
	return follow_users

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
		# user_object = User.objects.get(pk=user[0])
		user_songs = UserSong.objects.filter(user__pk=user[0])
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
	for user_songs in user_songs_array:
		age = [(datetime.datetime.now().date() - song.uploaded_at).days for song in user_songs]
		weighted_age = [1/(0.0005*(x+20)) for x in age]
		average = sum(weighted_age) / len(weighted_age)
		#Adjusts for effect
		weighted_age = [x - (x-average)*(1-recency_effect) for x in weighted_age]
		for song in range(number_songs):
			choice = weighted_choice(weighted_age)
			return_array[song].append(user_songs[choice])
	return return_array

	
def duplicate_artist(playlist,user_song):
	for song in playlist:
		if song.song.artists.name == user_song.song.artists.name:
			return True
	return False



def create_playlist(user,neighbors,follow_effect,number_songs,recency_effect,rating_effect,duplicate_artist_effect,existing_playlist_effect):
	'''Pass: the active user, number of neighbors to inform recommendation and
	 number of songs desired in playlist
	 Returns: Array of song objects '''
	#Ensures that the neighbors are limited while the userbase is small
	neighbors = int(min(neighbors,User.objects.all().count()/2))

	follow_list = [follower for follower in FollowList(user=user).following.all() if follower.song_set.exists()]
	follow_number = int(neighbors * follow_effect)
	reduced_neighbors = neighbors - follow_number
	if reduced_neighbors == 0:
		# pdb.set_trace()
		similar = [[None,1]]
	else:
		similar = similar_users(user,reduced_neighbors)
	if follow_number > 0:
		followees = follow_users(similar,follow_number,follow_list)
		follow_similar = similar + followees
		#HACKY
		follow_similar[0][0] = follow_similar [0][1]
	else:
		follow_similar = similar		
	playlist = []
	user_songs = get_user_song_array(follow_similar)
	song_choice = return_tracks_recency_bias(user_songs,number_songs,recency_effect)


	### Weighting factor 1, similarity to current user
	distances = [1/(x[1]+0.01) for x in similar]
	for song_number in song_choice:
		recommendation_array = []
		replication_array = []
		existing_playlist_array = []
		for user_song in song_number:
			### Weighting factor 2, user previous recommendations of artist
			recommendation = ArtistRating.objects.filter(user=user,artist=user_song.song.artists)
			if len(recommendation) == 1:
				score = float(recommendation[0].score)
			else:
				score = 0.5
			#Adjusts for effect
			score = score - (score-0.5)*(1-rating_effect)
			recommendation_array.append(score)
			### Weighting factor 3, no replicated artists in playlist
			if duplicate_artist(playlist,user_song) == True:
				replication_array.append(1-(duplicate_artist_effect))
			else:
				replication_array.append(1)
			### Weighting factor 4, already in user playlist
			existing = UserSong.objects.filter(user=user,song = user_song.song)
			if len(existing) == 1:
				existing_playlist_array.append(1-existing_playlist_effect)
			else:
				existing_playlist_array.append(1)
		#Multiply arrays
		final_weighting_array = []
		#change len(distances) to len(neighbors)
		for x in range(len(distances)):
			final_weighting  = distances[x] * recommendation_array[x] * replication_array[x] * existing_playlist_array[x]
			final_weighting_array.append(final_weighting)
		# Needs fixing to ensure that playlist is of conistent length
		if sum(final_weighting_array) == 0:
			continue
		### select song
		choice = weighted_choice(final_weighting_array)
		playlist.append(song_number[choice])
	return playlist











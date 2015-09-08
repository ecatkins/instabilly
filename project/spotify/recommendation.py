from spotify.models import User, UserProfile, UserSong, Song, Genre, Artist, ArtistRating, UserGenre, FollowList, NearestNeigh
from sklearn.neighbors import KNeighborsClassifier
import random
import datetime
import pdb


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


def get_user_song_array(users):
	user_songs_array = []
	for user in users:
		# user_object = User.objects.get(pk=user[0])
		user_songs = UserSong.objects.filter(user=user[0])
		user_songs_array.append(user_songs)
	return user_songs_array

def return_tracks_recency_bias(user_songs_array,number_songs,recency_effect):
	return_array = []
	extended_number_songs = int(number_songs*1.5)
	for x in range(extended_number_songs):
		return_array.append([])
	for user_songs in user_songs_array:
		age = [(datetime.datetime.now().date() - song.uploaded_at).days for song in user_songs]
		weighted_age = [1/(0.0005*(x+20)) for x in age]
		average = sum(weighted_age) / len(weighted_age)
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

def duplicate_song(playlist,user_song):
	for song in playlist:
		if song.song.track_uri == user_song.song.track_uri:
			return True
		return False



def get_neighbors(user,num_reduced_neighbors):
	user_profile = UserProfile.objects.get(user=user)
	users_neighbors = NearestNeigh.objects.filter(user=user_profile).order_by('distance')[:num_reduced_neighbors]
	neighbor_list = []
	for neighbor in users_neighbors:
		neighbor_user_object = neighbor.neighbor
		distance = neighbor.distance
		neighbor_list.append([neighbor_user_object,distance])
	return neighbor_list

def get_following(neighbors,follow_number,follow_list):
	if neighbors == None:
		neighbor_distance_average = 1
	else:
		neighbor_distance_average = sum([x[1] for x in neighbors]) / len(neighbors)
	follow_users = []
	for x in range(follow_number):
		random_follow_id = random.choice(follow_list).pk
		follow_users.append([random_follow_id,neighbor_distance_average])
	return follow_users

def create_playlist(user,num_neighbors,follow_effect,number_songs,recency_effect,rating_effect,duplicate_artist_effect,existing_playlist_effect):
	'''Pass: the active user, number of neighbors to inform recommendation and
	 number of songs desired in playlist
	 Returns: Array of song objects '''
	#Ensures that the neighbors are limited while the userbase is small
	num_neighbors = int(min(num_neighbors,User.objects.all().count()/2))
	follow_list = [follower for follower in FollowList(user=user).following.all() if follower.song_set.exists()]
	num_follow = int(num_neighbors * follow_effect)
	num_reduced_neighbors = num_neighbors - num_follow
	
	if num_reduced_neighbors == 0:
		neighbors = None
	else:
		neighbors = get_neighbors(user,num_reduced_neighbors)
	
	if num_follow > 0: 
		following = get_following(neighbors,num_follow,follow_list)
		if neighbors == None:
			following_and_neighbors = following
		else:
			following_and_neighbors = following + neighbors
	else:
		following_and_neighbors = neighbors

	playlist = [] 

	user_songs = get_user_song_array(following_and_neighbors)
	song_choice = return_tracks_recency_bias(user_songs,number_songs,recency_effect)


	### Weighting factor 1, similarity to current user
	distances = [1/(x[1]+0.01) for x in following_and_neighbors]
	for song_number in song_choice:
		if len(playlist) < number_songs:
			recommendation_array = []
			replication_array = []
			existing_playlist_array = []
			duplicate_song_array = []
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
				if len(existing) > 0:
					song = UserSong.objects.filter(user=user,song = user_song.song)
					existing_playlist_array.append(1-existing_playlist_effect)
				else:
					existing_playlist_array.append(1)
				### Final check to ensure no duplicate songs
				if duplicate_song(playlist,user_song) == True:
					duplicate_song_array.append(0)
				else:
					duplicate_song_array.append(1)
			#Multiply arrays
			final_weighting_array = []
			#change len(distances) to len(neighbors)
			for x in range(len(distances)):
				# print(x)
				final_weighting  = distances[x] * recommendation_array[x] * replication_array[x] * existing_playlist_array[x] * duplicate_song_array[x]
				final_weighting_array.append(final_weighting)
			# Needs fixing to ensure that playlist is of conistent length
			if sum(final_weighting_array) == 0:
				continue
			### select song
			
			choice = weighted_choice(final_weighting_array)
			playlist.append(song_number[choice])
		else:
			break
		
		# for i, item in enumerate(song_number):
		# 	print("SONG")
		# 	print(item.song.artists.name,item.song.track_name)
		# 	print("DISTANCE")
		# 	print(distances[i])
		# 	print("RECOMMENDATION")
		# 	print(recommendation_array[i])
		# 	print("REPLICATE ARTIST")
		# 	print(replication_array[i])
		# 	print("EXISTING PLAYLIST")
		# 	print(existing_playlist_array[i])
		# 	print("DUPLICATE SONG")
		# 	print(duplicate_song_array[i])
		# 	print("FINAL WEIGHTING")
		# 	print(final_weighting_array[i])		
		# 	print("")
		
		# print("WINNER")
		# print(song_number[choice].song.artists.name,song_number[choice].song.track_name)
		# print("")

	return playlist











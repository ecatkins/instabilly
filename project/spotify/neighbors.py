from spotify.models import User, UserProfile, UserGenre, Genre, NearestNeigh, UserSong 
from sklearn.neighbors import KNeighborsClassifier
import random
import pdb

def similar_users(user,genre_arrays,neighbors):
	''' Pass: the active user object and the number of neighbors to calculate
		Returns: An array of similar users, containing the username and the distance to that user on the genre-dimensional plot
	 '''
	# if user.pk == 18:
	# 	pdb.set_trace()
	id_array, x_array = genre_arrays
	copy_id_array = id_array.copy()
	copy_x_array = x_array.copy()	
	user_id = user.pk
	id_index = copy_id_array.index(user_id)
	user_array = copy_x_array[id_index]
	del copy_id_array[id_index]
	del copy_x_array[id_index]
	if len(copy_x_array) < neighbors:
		neighbors = len(copy_x_array)
	y_array = [random.random() for x in range(len(copy_x_array))]
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(copy_x_array, y_array)
	result = neigh.kneighbors(user_array,neighbors)
	similar_users = [[copy_id_array[result[1][0][x]],result[0][0][x]] for x in range(neighbors)]
	return similar_users



def get_genre_arrays():
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
	### I can change this???? Just to append array everytime

	for row in all_user_genres:
		if row['user_id'] != current_user_id:
			id_array.append(row['user_id'])
			x_array.append([0] * genre_count)
			counter += 1
			current_user_id = row['user_id']
			array = x_array[counter]
		array[zipped_genre_dictionary[row['genre_id']]] = row['proportion']
	return id_array, x_array


def update_users(user_list,neighbors=10):
	genre_arrays = get_genre_arrays()
	for user in user_list:
		print(user.pk)
		user_profile = UserProfile.objects.get(user=user)
		existing_neighbors = NearestNeigh.objects.filter(user=user_profile)
		existing_neighbors.delete()
		neighbor_array = similar_users(user,genre_arrays,neighbors)
		for neighbor in neighbor_array:
			neighbor_id = neighbor[0]
			neighbor_distance = neighbor[1]
			neighbor_user_object = User.objects.get(pk=neighbor_id)
			new_neighbor = NearestNeigh(user=user_profile,neighbor=neighbor_user_object,distance=neighbor_distance)
			new_neighbor.save()
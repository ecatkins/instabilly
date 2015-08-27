from sklearn.neighbors import KNeighborsClassifier
from spotify.models import User, Genre, UserGenre, UserSong
import random



def test(username,neighbors=5):
	name_array = []
	x_array = []
	all_users = User.objects.exclude(username=username)
	user = User.objects.get(username=username)
	# all_users = User.objects.all()
	genre_count = Genre.objects.count()
	# hold = list(UserGenre.objects.all())
	for other_user in all_users:
		print('b4 genre proportion')
		genre_array = genre_user_array(other_user, genre_count)
		if genre_array:
			print('scipy set up')
			name_array.append(other_user.username)
			x_array.append(genre_array)
	y_array = [random.random() for x in range(len(x_array))]
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	neigh.fit(x_array, y_array)
	user_genres = genre_user_array(user, genre_count)
	result = neigh.kneighbors((user_genres),neighbors)
	similar_users = [[name_array[result[1][0][x]],result[0][0][x]] for x in range(neighbors)]
	return similar_users


def genre_user_array(user, genre_count):
	if not UserSong.objects.filter(user=user).exists():
		return False
	else:
		genre_array = [0] * genre_count
		user_genre = UserGenre.objects.filter(user=user) 
		for genre in user_genre:
			genre_array[genre.genre.pk-1] = genre.proportion
		return genre_array


# test('adamrj')
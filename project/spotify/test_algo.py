from sklearn.neighbors import KNeighborsClassifier
import random

def test(users=1000000,neighbors=5):
	x_array = []
	for x in range(users):
		genre_array = []
		for y in range(700):
			genre_array.append(random.randrange(0,100))
		x_array.append(genre_array)
	y_array = [random.randrange(0,100) for x in range(users)]
	print("neighbors")
	neigh = KNeighborsClassifier(n_neighbors=neighbors)
	print("knights of neegh")
	neigh.fit(x_array, y_array)
	print("shrubbery")
	test = [random.randrange(0,100) for x in range(700)]
	result = neigh.kneighbors(test,neighbors)
	print(result)

test()




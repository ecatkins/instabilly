import sys
import os
import json

import django
import random






os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()


from spotify.models import TestModel

new_test = TestModel(number=random.randrange(1,100))
new_test.save()




#Could segment in future
# def user_list(type=None):
# 	all_users = User.objects.all()
# 	return all_users


# def update_users():
# 	users = user_list()
# 	for x in



# def similar_users(user,neighbors):
# 	''' Pass: the active user object and the number of neighbors to calculate
# 		Returns: An array of similar users, containing the username and the distance to that user on the genre-dimensional plot
# 	 '''
# 	# pdb.set_trace()
# 	id_array, x_array,user_array = get_genre_arrays(user)
# 	y_array = [random.random() for x in range(len(x_array))]
# 	neigh = KNeighborsClassifier(n_neighbors=neighbors)
# 	neigh.fit(x_array, y_array)
# 	result = neigh.kneighbors(user_array,neighbors)
# 	similar_users = [[id_array[result[1][0][x]],result[0][0][x]] for x in range(neighbors)]
# 	return similar_users




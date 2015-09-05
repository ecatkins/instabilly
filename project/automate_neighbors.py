import sys
import os
import json
import django
import datetime
from spotify.secret import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

django.setup()

from spotify.neighbors import *

# from spotify.models import User

start_time = datetime.datetime.now()

all_users = User.objects.all()

users_with_songs = []



for user in all_users:
	songs = UserSong.objects.filter(user=user)
	if len(songs) > 0:
		users_with_songs.append(user)

update_users(users_with_songs)

end_time = datetime.datetime.now()

time_delta = end_time - start_time

current_time = str(end_time)
benchmark = str(time_delta)


x = "Time of update: {0} \nTime to complete: {1}\n".format(current_time,time_delta)


current_directory = os.getcwd()

print(current_directory)

directory_string = current_directory + "/automatelogfile.txt"

with open(directory_string,'a') as myfile:
	myfile.write(x)





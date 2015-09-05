import sys
import os
import json
import django
import datetime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()

from spotify.neighbors import *

# from spotify.models import User

all_users = User.objects.all()

users_with_songs = []

for user in all_users:
	songs = UserSong.objects.filter(user=user)
	if len(songs) > 0:
		users_with_songs.append(user)

update_users(users_with_songs)

f = open('/Users/ecatkins/Dropbox/Coding/byte_academy/instabilly/project/workfile.txt', 'w')

current_time = str(datetime.datetime.now())

f.write(current_time)





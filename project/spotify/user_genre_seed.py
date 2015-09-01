from spotify.models import User, Genre, UserGenre, UserSong, UserProfile
import datetime

# testuser = User.objects.get(username="ecatkins")

def seed_one_user(user):
	all_genre_names = [x.name for x in Genre.objects.all()]
	genre_array = [0]*len(Genre.objects.all())
	user_songs = UserSong.objects.filter(user=user)
	number_songs = max(1,len(user_songs))
	for song in user_songs:
		artist = song.song.artists
		genres = artist.genres.all()
		for genre in genres:
			index = all_genre_names.index(genre.name)
			genre_array[index] += 1
	genre_percent_array = [x/number_songs for x in genre_array]
	for index, genre_name in enumerate(all_genre_names):
		genre = Genre.objects.get(name=genre_name)
		user_genre_object = UserGenre.objects.filter(user=user,genre=genre)
		if len(user_genre_object) == 0:
			new_object = UserGenre(user=user,genre=genre,proportion = genre_percent_array[index])
			new_object.save()
		else:
			old_object = user_genre_object[0]
			old_object.proportion = genre_percent_array[index]
			old_object.save()
	profile = UserProfile.objects.get(user=user)
	profile.updated_genres = datetime.datetime.now()
	profile.save()
	

def update_latest_user():
	all_user_profiles = UserProfile.objects.all().order_by('updated_genres')
	user = all_user_profiles[0].user
	seed_one_user(user)
	print(user.username)


# def quick_seed():
# 	eddy = User.objects.get(username="ecatkins")
# 	all_user_profiles = UserProfile.objects.exclude(user=eddy)
# 	for x in all_user_profiles:
# 		x.updated_genres = datetime.datetime.now()
# 		x.save()



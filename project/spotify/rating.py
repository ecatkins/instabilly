from spotify.models import ArtistRating, Artist, Song
import pdb

def wipe_ratings(user=None):
	if user == None:
		all_ratings = ArtistRating.objects.all()
		all_ratings.delete()
	else:
		user_ratings = ArtistRating.objects.filter(user=user)
		user_ratings.delete()

def update_ratings(user,track_uris,decision):
	rating_array = []
	for track in track_uris:
		full_uri = "spotify:track:" + track
		song_list = Song.objects.filter(track_uri=full_uri)
		song = song_list[0]
		artist = song.artists
		current_rating = ArtistRating.objects.filter(user=user,artist=artist)
		if len(current_rating) == 1:
			rating = float(current_rating[0].score)
		else:
			rating = 0.5
			
		rating_array.append([artist,rating])

	for index, element in enumerate(rating_array):
		copy_array = rating_array.copy()
		del copy_array[index]
		playlist_length = len(rating_array)
		PA = element[1]

		if decision == "like":
			count_PXA = 1
			count_PXnotA = 0
			for i in copy_array:
				count_PXA += i[1]
				count_PXnotA += i[1]
		else:
			count_PXA = 0
			count_PXnotA = 1
			for i in copy_array:
				count_PXA += (1-i[1])
				count_PXnotA += (1 - i[1])
		prob_A = PA * (count_PXA/playlist_length)
		prob_notA = (count_PXnotA / playlist_length) * (1 - PA)
		new_rating = prob_A/(prob_A + prob_notA)

		artist_rating, created = ArtistRating.objects.get_or_create(user=user, artist=element[0])
		artist_rating.score = new_rating
		artist_rating.save()
	return True













from spotify.models import ArtistRecommendation, Artist, Song

def wipe_ratings(user=None):
	if user = None:
		all_ratings = ArtistRecommendation.objects.all()
		all_ratings.delete()
	else:
		user_ratings = ArtistRecommendation.objects.filter(user=user)
		user_ratings.delete()

def update_ratings(user,track_uris,decision):
	rating_array = []
	for track in track_uris:
		full_uri = "spotify:track:" + track
		song = Song.objects.get(track_uri=full_uri)
		artist = song.artists
		current_rating = ArtistRecommendation.objects.filter(user=user,artist=artist)
		if len(current_rating) == 0:
			rating = 0.5
		else:
			rating = current_rating[0].score
		rating_array.append([artist,rating])

	for index, element in enumerate(rating_array):
		# P(A) = rating
		# P(P|A)
		# P()
		copy_array = rating_array.copy()
		playlist_length = len(rating_array)
		del copy_array[index]
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
			prob_notA = count_PXnotA * (1 - PA)
			new_rating = prob_A/(prob_A + prob_notA)

		aritst_rec = ArtistRecommendation.objects.get(user=user, artist=element[0])
		artist_rec.score = new_rating
		artist_rec.save()













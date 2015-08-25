from spotify.models import ArtistRecommendation

def wipe_ratings(user=None):
	if user = None:
		all_ratings = ArtistRecommendation.objects.all()
		all_ratings.delete()
	else:
		user_ratings = ArtistRecommendation.objects.filter(user=user)
		user_ratings.delete()

def update_ratings(user,track_uris,decision):
	pass
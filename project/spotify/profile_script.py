from spotify.models import User, UserProfile

def seedprofile():
    all_users = User.objects.all()
    for user in all_users:
        profile = UserProfile.objects.filter(user=user)
        if len(profile) == 0:
            new_profile = UserProfile(user=user, is_real=True)
            new_profile.save()
            
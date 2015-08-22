from spotify.models import User, Profile

def seedprofile():
    all_users = User.objects.all()
    for user in all_users:
        profile = Profile.objects.filter(user=user)
        if len(profile) == 0:
            new_profile = Profile(user=user, is_real=True)
            new_profile.save()
            
from spotify.models import User, FollowList

def followlist():
    all_users = user.objects.all()
    for user in all_users:
        new_followlist = FollowList(user=user)
        new_followlist.save()

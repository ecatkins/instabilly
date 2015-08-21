from spotify.models import User, FollowList

def seedfollowlist():
    all_users = User.objects.all()
    for user in all_users:
        follow_list = FollowList.objects.filter(user=user)
        if len(follow_list) == 0:
            new_follow_list = FollowList(user=user)
            new_follow_list.save()
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import View
import spotipy
from spotipy import oauth2
import spotipy.util as util
import requests
from spotify.secret import *
from spotify.models import Song, User, UserSong, UserProfile, UserActivationCode, FollowList, Artist, Post
from spotify.forms import UserForm, RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from spotify.seedgenre import seed_genre
import datetime
import pdb
from spotify.recommendation import *
from spotify.rating import *
from spotify.user_genre_seed import *
from spotify.neighbors import *
import random


class HomeView(View):
    template = "spotify/home.html"

    def get(self, request):
        return render(request, self.template, {"login_form": UserForm(), "registration_form": RegistrationForm()})


class RegistrationView(View):

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            hashed_password = make_password(password)
            user = User(username=username, password=hashed_password, first_name=first_name, last_name=last_name, email=email)
            user.save()
            request.session['session_id'] = user.pk
            follow_list = FollowList(user=user)
            follow_list.save()
            user_activation = UserActivationCode(user=user)
            user_activation.save()
            profile = UserProfile(user=user, updated_genres=datetime.datetime.now())
            profile.save()
            request.session['post_oauth'] = 'timeline'

            ###testing email#######
            # subject = "Confirm your registration"
            # message = "You're almost there! Copy and paste this code into the activation page: {}".format(user_activation.code)
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [user.email, settings.EMAIL_HOST_USER]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            # print("sent mail!!!")
            # return redirect("activation")
            #####email########
            return redirect("oauth")
        else:
            errors = registration_form.errors.as_json()
            return render(request, 'spotify/home.html', {"login_form": UserForm(), "registration_form": registration_form,"registration_error": "Invalid Registration Details"})


            

class ActivationView(View):
    template = "spotify/activation.html"

    def get(self, request):
        request.session['post_oauth'] = 'timeline'
        return render(request, self.template)


class LoginView(View):

    def post(self, request): 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if len(user) == 1 and check_password(password, user[0].password):
            request.session['session_id'] = user[0].pk
            request.session['post_oauth'] = 'timeline'
            return redirect("oauth")
        else:
            return render(request, 'spotify/home.html', {"login_form": UserForm(), "login_error": "Invalid Credentials", "registration_form": RegistrationForm()})


class LogoutView(View):

    def get(self, request):
        request.session.flush()
        return redirect('/')


class OauthView(View):

    ####USE THIS FOR TESTING WITHOUT EMAIL ACTIVATION#####
    def get(self,request):
        x = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope="playlist-read-private user-library-read user-library-modify playlist-modify-public playlist-modify-private")
        url = x.get_authorize_url()
        return redirect(url)

    ###USE FOR TESTING WITH EMAIL ACTIVATION######
    # def get(self,request):
    #     userprofile = UserProfile.objects.filter(user__pk=request.session['session_id'])
    #     userprofile_obj = userprofile[0]

    #     if userprofile_obj.verified == True:
    #         x = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope="playlist-read-private user-library-modify playlist-modify-public playlist-modify-private")
    #         url = x.get_authorize_url()
    #         return redirect(url)
    #     else:
    #         user_activation = UserActivationCode.objects.get(user__pk=request.session['session_id'])
    #         email_activation_code = request.GET.get('activation_code')
    #         if str(user_activation.code) == email_activation_code:
    #             userprofile_obj.verified = True
    #             print('before save, is verified = ', userprofile_obj.verified)
    #             testsave = userprofile_obj.save()
    #             x = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope="playlist-read-private user-library-modify playlist-modify-public playlist-modify-private")
    #             url = x.get_authorize_url()
    #             return redirect(url)



class CallbackView(View):

    def get(self,request):
        code = request.GET.get('code')
        request.session['spotify_code'] = code
        return redirect('timeline')
        # if request.session['post_oauth'] == 'timeline':
        # elif request.session['post_oauth'] == 'seed_user_library':
        #     return redirect('seed')


class TimelineView(View):
    template = "spotify/index.html"

    def get(self,request):
        user = User.objects.filter(pk=request.session['session_id'])
        followlist_obj = FollowList.objects.filter(user=user[0])
        follow_list = followlist_obj[0].following.all()
        exclude_list = list(follow_list) + list(user)
        post_list = Post.objects.exclude(user__in=exclude_list).order_by('-created_at')[:20]
        followers = FollowList.objects.filter(following=user[0])
        following_count = len(follow_list)
        followers_count = len(followers)
        song_count = UserSong.objects.filter(user=user[0]).count()
        username = user[0].username.upper()
        user_post_list = Post.objects.filter(user=user[0]).order_by('-created_at')
        latest_post = Post.objects.filter(user=user[0]).order_by('-created_at')[:1]
        if len(latest_post) == 1:
            latest_post_track = latest_post[0].song.song.track_uri
            latest_post_date = latest_post[0].created_at
            today = datetime.datetime.now().date()
            readable_date = latest_post_date.strftime('%b %d')
            readable_time = latest_post_date.strftime('%I:%M%p')
            if today.strftime('%d/%m/%Y') == latest_post_date.strftime('%d/%m/%Y'):
                time = readable_time
            else:
                time = readable_date
            return render(request, self.template, {"latest_post_track": latest_post_track, "latest_post_date": time, "follow_list": follow_list, "followers": followers,"user_post_list": user_post_list, "post_list": post_list,"following_count":following_count,"followers_count":followers_count,"song_count":song_count,"username":username})
        else:
            return render(request, self.template, {"no_post": "NONE","follow_list": follow_list, "followers": followers, "post_list": post_list,"following_count":following_count,"followers_count":followers_count,"song_count":song_count,"username":username})


class UpdateProfileView(View):

    def get(self,request):
        user = User.objects.get(pk=request.session['session_id'])
        user_song_count = UserSong.objects.filter(user=user).count()
        follow_list = FollowList.objects.get(user=user)
        following_count = follow_list.following.all().count()
        followers_count = FollowList.objects.filter(following=user).count()
        return JsonResponse(({"song_count":user_song_count,"following_count":following_count,"followers_count":followers_count}))


class HasSongsView(View):

    def get(self,request):
        user = User.objects.get(pk=request.session['session_id'])
        has_songs = UserSong.objects.filter(user=user).exists()
        return JsonResponse({"has_songs":has_songs})

class GetFollowingView(View):

    def get(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        JSON_follow_list = []
        for item in user_follow_list[0].following.all():
            JSON_follow_list.append(item.username)
        return JsonResponse({"JSON_follow_list": JSON_follow_list})


class FollowView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        following = User.objects.filter(username=request.POST['id'])
        user_follow_list[0].following.add(following[0])
        return JsonResponse({"user": user[0].username, "following": following[0].username})


class UnfollowView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        unfollow = User.objects.filter(username=request.POST['id'])
        user_follow_list[0].following.remove(unfollow[0])
        return JsonResponse({"user": user[0].username, "unfollow": unfollow[0].username})


class SearchView(View): 

        def get(self, request):
            query = request.GET.get('search_query').lower()
            user = User.objects.filter(pk=request.session['session_id'])
            usersongs = UserSong.objects.filter(user=user[0])
            search_result = []
            for item in usersongs:
                if query in item.song.track_name.lower():
                    search_result.append(item.song.track_name)
            if len(search_result) > 0:
                return JsonResponse({"search_result": search_result})
            else:
                return JsonResponse({"search_result": ["No results found..."]})

class FindUserView(View):

    def get(self, request):
        search_query = request.GET.get("usernameQuery").lower()
        if search_query != "":
            all_users = User.objects.all()
            currentuser = User.objects.filter(pk=request.session['session_id'])
            search_result = []
            for user in all_users:
                if (search_query in user.username.lower()) and (search_query != currentuser[0].username):
                    search_result.append(user.username)
            if len(search_result) > 0:
                return JsonResponse({"search_result": search_result})
            else:
                return JsonResponse({"search_result": "No results found..."})
        else:
            return JsonResponse({"search_result": "Please input a username."})
   

class TrackURIView(View):

    def get(self, request):
        track_name = request.GET.get('track_name')
        song = Song.objects.filter(track_name=track_name)
        track_uri = song[0].track_uri
        return JsonResponse({"track_uri": track_uri})

class CreatePostView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        track_uri = request.POST.get('track_uri')
        content = request.POST.get('comment')
        song = Song.objects.filter(track_uri=track_uri)
        usersong = UserSong.objects.filter(user=user, song=song)
        new_post = Post(user=user[0], song=usersong[0], content=content)
        new_post.save()
        readable_time = new_post.created_at.strftime('%I:%M%p')
        readable_datetime = new_post.created_at.strftime('%b %d, %I:%M%p')
        return JsonResponse({"status": "success", "time": readable_time, "datetime": readable_datetime, "track_uri": new_post.song.song.track_uri, "id": new_post.pk})

class DeletePostView(View):

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.filter(pk=post_id)
        post[0].delete()
        return JsonResponse({"post": "DELETED"})


class GetMiniFeedView(View):

    def get(self, request):
        time_zone_offset = int(request.GET.get('timeZoneOffset'))
        user = User.objects.filter(pk=request.session['session_id'])
        user_followlist_obj = FollowList.objects.filter(user=user[0])
        follow_list = user_followlist_obj[0].following.all()
        JSON_all_posts = []            
        all_posts = Post.objects.all().exclude(user=user[0]).order_by('-created_at')
        for post in all_posts:
            if len(JSON_all_posts) <= 20:
                if post.user in follow_list:
                    today_adj_datetime = datetime.datetime.now() - datetime.timedelta(minutes=time_zone_offset)
                    post_adj_datetime = post.created_at - datetime.timedelta(minutes=time_zone_offset)
                    today_date = today_adj_datetime.date()
                    post_date = post_adj_datetime.date()
                    if today_date.strftime('%d/%m/%Y') == post_date.strftime('%d/%m/%Y'):
                        readable_datetime = post_adj_datetime.strftime('%I:%M%p')
                    else:
                        readable_datetime = post_adj_datetime.strftime('%b %d, %Y %I:%M%p')
                    post_dict = {"user": post.user.username, "track_uri": post.song.song.track_uri, "created_at": readable_datetime, "content": post.content}
                    JSON_all_posts.append(post_dict)
            else:
                break
        return JsonResponse({"all_posts": JSON_all_posts})


def save_songs(song_list, user):
    save_count = 0
    for item in song_list:
        try:
            duplicate_songs = Song.objects.filter(track_id=item['track']['id'])
            if len(duplicate_songs) == 0:
                artist_search = Artist.objects.filter(name=item['track']['artists'][0]['name'])
                if len(artist_search) == 1:
                    artist = artist_search[0]
                else:
                    artist_name = item['track']['artists'][0]['name']
                    artist = seed_genre(artist_name)
                song = Song(track_name=item['track']['name'], track_id=item['track']['id'], track_uri=item['track']['uri'], artist_id=item['track']['artists'][0]['id'], album=item['track']['album']['name'], album_id=item['track']['album']['id'], album_uri=item['track']['album']['uri'], spotify_popularity=item['track']['popularity'], preview_url=item['track']['preview_url'], image_300=item['track']['album']['images'][1]['url'], image_64=item['track']['album']['images'][2]['url'], artists=artist)
                date_added = datetime.datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                print(date_added)
                song.save()
                usersong = UserSong(user=user, song=song, uploaded_at=date_added)
                usersong.save()
                print("Saved New Song: {0}".format(song.track_name))
                save_count += 1
            else:
                date_added = datetime.datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                duplicate_user_songs = UserSong.objects.filter(song=duplicate_songs[0],user=user,uploaded_at=date_added)
                if len(duplicate_user_songs) == 0:
                    usersong = UserSong(user=user,song=duplicate_songs[0], uploaded_at=date_added)
                    usersong.save()
                    print("Saved New User Song: {0}".format(usersong.song.track_name))
        except:
            continue
    return save_count


def get_user_saved_tracks(sp, user):
    saved_results = sp.current_user_saved_tracks(limit=1)
    count = 0
    while count < saved_results['total']:
        results = sp.current_user_saved_tracks(limit=50,offset=count)
        count += 50
        saved_songs = save_songs(results['items'], user)
    return True

def get_user_playlist_tracks(sp, user):
    username = sp.current_user()['id']
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
    	if playlist['owner']['id'] == username:
            playlist_results = sp.user_playlist_tracks(username, playlist['id'],
                fields="total,items")
            count = 0
            while count < playlist_results['total']:
                results = sp.user_playlist_tracks(username, playlist['id'],limit=50,offset=count,fields="total, items")
                count += 50
                saved_songs = save_songs(results['items'], user)
    return True



def get_user_token(request):
    post_route = "https://accounts.spotify.com/api/token"
    callback = SPOTIPY_REDIRECT_URI
    grant_type = "authorization_code"
    code = request.session['spotify_code']
    pay_load = {"grant_type":grant_type, "code":code, "redirect_uri":callback,"client_id":SPOTIPY_CLIENT_ID,"client_secret":SPOTIPY_CLIENT_SECRET}
    r = requests.post(post_route,data=pay_load)
    print(r)
    token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']
    request.session['access_token'] = token
    request.session['refresh_token'] = refresh_token
    del request.session['spotify_code']
    return token

def refresh_token(request):
    grant_type = "refresh_token"
    post_route = "https://accounts.spotify.com/api/token"
    refresh_token = request.session['refresh_token']
    callback = SPOTIPY_REDIRECT_URI
    pay_load = {"grant_type":grant_type, "refresh_token":refresh_token, "redirect_uri":callback,"client_id":SPOTIPY_CLIENT_ID,"client_secret":SPOTIPY_CLIENT_SECRET}
    r = requests.post(post_route,data=pay_load)
    print(r)
    token = r.json()['access_token']
    # refresh_token = r.json()['refresh_token']
    request.session['access_token'] = token
    # request.session['refresh_token'] = refresh_token
    return token

def get_spotipy_instance(request):
    try:
        token = get_user_token(request)
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id'] 
    except:
        try:
            token = request.session['access_token']
            sp = spotipy.Spotify(auth=token)
            username = sp.current_user()['id']
        except:
            try:
                token = refresh_token(request)
                sp = spotipy.Spotify(auth=token)
                username = sp.current_user()['id']
            except:
                return False
    return sp,username



class SeedUserLibraryView(View):
    def get(self, request):
        spotipy = get_spotipy_instance(request)
        if spotipy != False:
            sp,username = spotipy
            user = User.objects.get(pk=request.session['session_id'])
            saved_tracks = get_user_saved_tracks(sp, user)
            playlist_tracks = get_user_playlist_tracks(sp, user)
            seed_one_user(user)
            update_users([user])
            return JsonResponse({"status":"Success"})
        else:
            request.session['post_oauth'] = 'seed_user_library'
            return JsonResponse({"status":"Failure"})



class EngineView(View):
    template = "spotify/recommendation_engine.html"

    def get(self,request):
        return render(request,self.template)

class PlaylistView(View):

    def post(self,request):
        user = User.objects.get(pk=request.session['session_id'])
        playlist_type = request.POST.get("type")
        number_songs = int(request.POST.get('number_songs'))
        neighbors = 10
        follow_effect = int(request.POST.get('follow'))/10.0
        recency_effect = int(request.POST.get('recency_effect'))/10.0
        rating_effect = int(request.POST.get('rating_effect'))/10.0
        duplicate_artist = int(request.POST.get('duplicate_artist'))/10.0
        existing_playlist = int(request.POST.get('existing_playlist'))/10.0
        playlist = create_playlist(user=user,num_neighbors=neighbors, follow_effect=follow_effect, number_songs=number_songs,recency_effect=recency_effect,rating_effect=rating_effect,duplicate_artist_effect=duplicate_artist,existing_playlist_effect=existing_playlist)
        track_uris = []
        cover_track_uri = playlist[0].song.track_uri
        for song in playlist:
            track_uris.append(song.song.track_uri[-22:])
        first_track = track_uris[0]
        first_track_object = Song.objects.filter(track_uri=cover_track_uri)
        cover_art = first_track_object[0].image_300
        return JsonResponse({"track_uris":track_uris,"cover_art":cover_art})
    
class RatingView(View):

    def post(self, request):
        user = User.objects.get(pk=request.session['session_id'])
        decision = request.POST.get('decision')
        track_uris = request.POST.getlist('uris[]')
        status = update_ratings(user,track_uris,decision)
        return JsonResponse({"status": "Success"})


class SavePlaylistView(View):
   
    def post(self,request):
        sp,username = get_spotipy_instance(request)
        name = "MoneyMusic Playlist {0}".format(random.randrange(1,1000))
        new_playlist = sp.user_playlist_create(username,name)
        new_playlist_id = new_playlist['id']
        track_uris = request.POST.getlist('uris[]')
        full_track_uris = ["spotify:track:" + track for track in track_uris]
        sp.user_playlist_add_tracks(username,new_playlist_id,full_track_uris)
        return JsonResponse({"Success":"success"})


class SaveSongView(View):

    def post(self, request):
        sp, username = get_spotipy_instance(request)
        track_uri = request.POST.get('track_uri')
        track_uri_list = [track_uri]
        sp.current_user_saved_tracks_add(track_uri_list)
        return JsonResponse({"status": "success"})


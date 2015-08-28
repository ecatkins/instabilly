from django.shortcuts import render, redirect
from django.views.generic import View
import spotipy
from spotipy import oauth2
import spotipy.util as util
import requests
from spotify.secret import *
from spotify.models import Song, User, UserSong, UserProfile, FollowList, Artist, Post
from spotify.forms import UserForm, RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from spotify.seedgenre import seed_genre
import datetime
import pdb
from spotify.recommendation import *
from spotify.rating import *
from spotify.user_genre_seed import *


class HomeView(View):
    template = "spotify/home.html"

    def get(self, request):
        return render(request, self.template, {"login_form": UserForm(), "registration_form": RegistrationForm()})



class RegistrationView(View):

    def post(self, request):
        print('in registration view')
        registration_form = RegistrationForm(request.POST)
        print(registration_form)
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
            profile = UserProfile(user=user, is_real=True, updated_genres=datetime.datetime.now())
            profile.save()
            return redirect("oauth")
        else:
            errors = registration_form.errors.as_json()
            # return render(request, 'spotify/home.html', {"login_form": UserForm(), "registration_form": registration_form})
            return JsonResponse({"errors": errors})

class LoginView(View):

    def post(self, request): 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if len(user) == 1 and check_password(password, user[0].password):
            request.session['session_id'] = user[0].pk
            return redirect("oauth")
        else:
            return render(request, 'spotify/home.html', {"login_form": UserForm(), "login_error": "Invalid credentials.", "registration_form": RegistrationForm()})


class LogoutView(View):

    def get(self, request):
        request.session.flush()
        return redirect('/')


class OauthView(View):

    def get(self,request):
        x = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope="playlist-read-private user-library-modify playlist-modify-public playlist-modify-private")
        url = x.get_authorize_url()
        return redirect(url)


class SyncView(View):
    template = "spotify/index.html"

    def get(self,request):
        code = request.GET.get('code')
        request.session['spotify_code'] = code
        user = User.objects.filter(pk=request.session['session_id'])
        followlist_obj = FollowList.objects.filter(user=user[0])
        follow_list = followlist_obj[0].following.all()
        post_list = Post.objects.all().order_by('-created_at')
        return render(request, self.template, {"follow_list": follow_list, "post_list": post_list})


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
        print("follow list after follow: ", user_follow_list[0].following.all())
        return JsonResponse({"user": user[0].username, "following": following[0].username})


class UnfollowView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        unfollow = User.objects.filter(username=request.POST['id'])
        user_follow_list[0].following.remove(unfollow[0])
        print("follow list after unfollow: ", user_follow_list[0].following.all())
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
        return JsonResponse({"status": "success"})

class GetMiniFeedView(View):

    def get(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_followlist_obj = FollowList.objects.filter(user=user[0])
        follow_list = user_followlist_obj[0].following.all()
        JSON_all_posts = []            
        all_posts = Post.objects.all().exclude(user=user[0]).order_by('-created_at')
        for post in all_posts:
            if post.user in follow_list:
                post_dict = {"user": post.user.username, "track_uri": post.song.song.track_uri, "created_at": post.created_at, "content": post.content}
                JSON_all_posts.append(post_dict)
        return JsonResponse({"all_posts": JSON_all_posts[:5]})


def save_songs(song_list, user):
    save_count = 0
    for item in song_list:
        try:
            duplicate_songs = Song.objects.filter(track_name=item['track']['name'])
            if len(duplicate_songs) == 0:
                artist_search = Artist.objects.filter(name=item['track']['artists'][0]['name'])
                if len(artist_search) == 1:
                    artist = artist_search[0]
                else:
                    artist_name = item['track']['artists'][0]['name']
                    artist = seed_genre(artist_name)
                song = Song(track_name=item['track']['name'], track_id=item['track']['id'], track_uri=item['track']['uri'], artist=item['track']['artists'][0]['name'], artist_id=item['track']['artists'][0]['id'], album=item['track']['album']['name'], album_id=item['track']['album']['id'], album_uri=item['track']['album']['uri'], spotify_popularity=item['track']['popularity'], preview_url=item['track']['preview_url'], image_300=item['track']['album']['images'][1]['url'], image_64=item['track']['album']['images'][2]['url'], artists=artist)
                date_added = datetime.datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                print(date_added)
                song.save()
                usersong = UserSong(user=user[0], song=song, uploaded_at=date_added)
                usersong.save()
                print("Saved New Song: {0}".format(song.track_name))
                save_count += 1
            else:
                date_added = datetime.datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ").date()
                duplicate_user_songs = UserSong.objects.filter(song=duplicate_songs[0],user=user[0],uploaded_at=date_added)
                if len(duplicate_user_songs) == 0:
                    usersong = UserSong(user=user[0],song=duplicate_songs[0], uploaded_at=date_added)
                    usersong.save()
                    print("Saved New User Song: {0}".format(usersong.song.track_name))
        except:
            continue
    return save_count


def get_user_saved_tracks(sp, user):
    print("saved")
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


class SeedUserLibraryView(View):

    def get(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        if len(user) == 1:
            post_route = "https://accounts.spotify.com/api/token"
            callback = SPOTIPY_REDIRECT_URI
            grant_type = "authorization_code"
            pay_load = {"grant_type":grant_type, "code":request.session['spotify_code'], "redirect_uri":callback,"client_id":SPOTIPY_CLIENT_ID,"client_secret":SPOTIPY_CLIENT_SECRET}
            r = requests.post(post_route,data=pay_load)
            token = r.json()['access_token']
            print(token)
            request.session['user_token'] = token
            sp = spotipy.Spotify(auth=token)
            saved_tracks = get_user_saved_tracks(sp, user)
            playlist_tracks = get_user_playlist_tracks(sp, user)
            seed_one_user(user)
            if saved_tracks & playlist_tracks:
                return JsonResponse({"status": "Success"})
            else:
                return JsonResponse({"status":"incomplete seed"})


class EngineView(View):
    template = "spotify/recommendation_engine.html"

    def get(self,request):
        return render(request,self.template)

class PlaylistView(View):

    def post(self,request):
        user = User.objects.get(pk=request.session['session_id'])
        playlist_type = request.POST.get("type")
        print(playlist_type)
        number_songs = int(request.POST.get('number_songs'))
        # neighbors = int(request.POST.get('neighbors'))
        neighbors = 5
        follow_effect = int(request.POST.get('follow'))/10.0
        recency_effect = int(request.POST.get('recency_effect'))/10.0
        rating_effect = int(request.POST.get('rating_effect'))/10.0
        duplicate_artist = int(request.POST.get('duplicate_artist'))/10.0
        existing_playlist = int(request.POST.get('existing_playlist'))/10.0
        playlist =create_playlist(user=user,neighbors=neighbors, follow_effect=follow_effect, number_songs=number_songs,recency_effect=recency_effect,rating_effect=rating_effect,duplicate_artist_effect=duplicate_artist,existing_playlist_effect=existing_playlist)    
        track_uris = []
        cover_track_uri = playlist[0].song.track_uri
        for song in playlist:
            track_uris.append(song.song.track_uri[-22:])
        if playlist_type == "your_home":
            print("here")
            first_track = track_uris[0]
            print(first_track)
            first_track_object = Song.objects.get(track_uri=cover_track_uri)
            print(first_track_object)
            cover_art = first_track_object.image_300
            print(cover_art)
            return JsonResponse({"track_uris":track_uris,"cover_art":cover_art})
        else:
            return JsonResponse({"track_uris":track_uris})

class RatingView(View):

    def post(self, request):
        user = User.objects.get(pk=request.session['session_id'])
        decision = request.POST.get('decision')
        track_uris = request.POST.getlist('uris[]')
        status = update_ratings(user,track_uris,decision)
        return JsonResponse({"status": "Success"})

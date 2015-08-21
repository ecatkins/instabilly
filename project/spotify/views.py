from django.shortcuts import render, redirect
from django.views.generic import View
import spotipy
from spotipy import oauth2
import spotipy.util as util
import requests
from spotify.secret import *
from spotify.models import Song, User, UserSong, Profile, FollowList, Artist
from spotify.forms import UserForm, RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from spotify.seedgenre import seed_genre
import pdb


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
            print('successful user save')
            return redirect("oauth")
        else:
            return render(request, 'spotify/home.html', {"login_form": UserForm(), "registration_form": registration_form})


class LoginView(View):

    def post(self, request): 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if len(user) == 1 and check_password(password, user[0].password):
            request.session['session_id'] = user[0].pk
            print(request.session['session_id'])
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
        user_list = User.objects.all().exclude(pk=request.session['session_id'])
        return render(request, self.template, {"user_list": user_list})


class GetFollowingView(View):

    def get(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        JSON_follow_list = []
        for item in user_follow_list[0].following.all():
            following.append(item.username)
        print(JSON_follow_list)
        return JsonResponse({"user_follow_list": JSON_follow_list})


class FollowView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        following = User.objects.filter(username=request.POST['username'])
        user_follow_list[0].following.add(following[0])
        return JsonResponse({"user": user[0].username, "following": following[0].username})


class UnfollowView(View):

    def post(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        user_follow_list = FollowList.objects.filter(user=user[0])
        unfollow = User.objects.filter(username=request.POST['username'])
        user_follow_list[0].following.remove(unfollow[0])
        return JsonResponse({"user": user[0].username, "unfollow": unfollow[0].username})


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
                song.save()
                print(song.track_name)
                print(user[0])
                print(song.track_name)
                usersong = UserSong(user=user[0], song=song)
                usersong.save()
                print("unique song success")
                save_count += 1
            else:
                duplicate_user_songs = UserSong.objects.filter(song=duplicate_songs[0],user=user[0])
                if len(duplicate_user_songs) == 0:
                    usersong = UserSong(user=user[0],song=duplicate_songs[0])
                    usersong.save()
                    print(duplicate_songs[0].track_name)
                    print("user song success")
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
    print("playlist")
    username = sp.current_user()['id']
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
    	print(playlist['name'])
    	if playlist['owner']['id'] == username:
            print("got here")
            playlist_results = sp.user_playlist_tracks(username, playlist['id'],
                fields="total,items")
            count = 0
            while count < playlist_results['total']:
                results = sp.user_playlist_tracks(username, playlist['id'],limit=50,offset=count,fields="total, items")
                count += 50
                saved_songs = save_songs(results['items'], user)
    return True

# spotify:user:11800860


class SeedUserLibraryView(View):

    def get(self, request):
        print("here")
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
            if saved_tracks & playlist_tracks:
                return JsonResponse({"status": "Success"})
            else:
                return JsonResponse({"status":"incomplete seed"})

# track_id=print(item['track']['id'])
# track_uri=print(item['track']['uri'])
# artist=print(item['track']['artists'][0]['name'])
# artist_id=print(item['track']['artists'][0]['id'])
# album=print(item['track']['album']['name'])
# album_id=print(item['track']['album']['id'])
# album_uri=print(item['track']['album']['uri'])
# spotify_popularity=print(item['track']['popularity'])
# preview_url=print(item['track']['preview_url'])
# image_300=print(item['track']['album']['images'][1]['url'])
# image_64=print(item['track']['album']['images'][2]['url'])


# song = Song(track_name="Ghost Ship", track_id="61JDaStnXY3vbaEjliB5WA", track_uri="spotify:track:61JDaStnXY3vbaEjliB5WA", artist="Blur", artist_id="7MhMgCo0Bl0Kukl93PZbYS", album="The Magic Whip", album_id="0nSzBICzQHea8grwfqa5Gb", album_uri="spotify:album:0nSzBICzQHea8grwfqa5Gb", spotify_popularity=56, preview_url="https://p.scdn.co/mp3-preview/250765ca652fc1b71c66ff17b5b7ffa3c7dbcfe6", image_300="https://i.scdn.co/image/9a19621ef5380cded361f5144dc5ad32332a3fad", image_64="https://i.scdn.co/image/ceb4e64d9f204b3553e48cfe1b879555d272fada")
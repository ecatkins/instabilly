from django.shortcuts import render, redirect
from django.views.generic import View
import spotipy
from spotipy import oauth2
import spotipy.util as util
import requests
from spotify.secret import *
from spotify.models import Song, User, UserSong, Profile
from spotify.forms import UserForm, RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password


class HomeView(View):
    template = "spotify/home.html"

    def get(self, request):
        return render(request, self.template, {"login_form": UserForm(), "registration_form": RegistrationForm()})



class RegistrationView(View): ####ADAM IS WORKING ON SPECIFIC ERROR MESSAGES FOR FIELDS

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
            return redirect("oauth")
        else:
            return render(request, 'spotify/home.html', {"login_form": UserForm(), "login_error": "Invalid credentials.", "registration_form": RegistrationForm()})


class LogoutView(View):

    def get(self, request):
        request.session.flush()
        return redirect('/')


class OauthView(View):

	def get(self,request):
		x = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,"http://127.0.0.1:8000/callback",scope="user-library-modify playlist-modify-public playlist-modify-private")
		url = x.get_authorize_url()
		return redirect(url)

class SyncView(View):
    template = "spotify/index.html"

    def get(self,request):
        code = request.GET.get('code')
        request.session['spotify_code'] = code
        return render(request, self.template)


def save_songs(song_list):
<<<<<<< HEAD
	save_count = 0
	for item in song_list:
		try:
			duplicate_songs = Song.objects.filter(track_name=item['track']['name'])
			if len(duplicate_songs) == 0:
				song = Song(track_name=item['track']['name'], track_id=item['track']['id'], track_uri=item['track']['uri'], artist=item['track']['artists'][0]['name'], artist_id=item['track']['artists'][0]['id'], album=item['track']['album']['name'], album_id=item['track']['album']['id'], album_uri=item['track']['album']['uri'], spotify_popularity=item['track']['popularity'], preview_url=item['track']['preview_url'], image_300=item['track']['album']['images'][1]['url'], image_64=item['track']['album']['images'][2]['url'])
				song.save()
				print(song.track_name)
				usersong = UserSong(user=user[0], song=song)
				usersong.save()
				print("usersong success")
				save_count += 1
			else:
				duplicate_user_songs = UserSong.objects.filter(song=duplicate_songs[0],user=user[0])
				if len(duplicate_user_songs) == 0:
			 		usersong = UserSong(user=user[0],song=duplicate_songs[0])
			 		usersong.save()
		except:
			continue
	return save_count
=======
    save_count = 0
    for item in song_list:
        try:
            duplicate_songs = Song.objects.filter(track_name=item['track']['name'])
            if len(duplicate_songs) == 0:
                song = Song(track_name=item['track']['name'], track_id=item['track']['id'], track_uri=item['track']['uri'], artist=item['track']['artists'][0]['name'], artist_id=item['track']['artists'][0]['id'], album=item['track']['album']['name'], album_id=item['track']['album']['id'], album_uri=item['track']['album']['uri'], spotify_popularity=item['track']['popularity'], preview_url=item['track']['preview_url'], image_300=item['track']['album']['images'][1]['url'], image_64=item['track']['album']['images'][2]['url'])
                song.save()
                print(song.track_name)
                usersong = UserSong(user=user[0], song=song)
                usersong.save()
                print("usersong success")
                save_count += 1
            else:
                duplicate_user_songs = UserSong.objects.filter(song=duplicate_songs[0],user=user[0])
                if len(duplicate_user_songs) == 0:
                    usersong = UserSong(user=user[0],song=duplicate_songs[0])
                    usersong.save()
        except:
            continue
    return save_count
>>>>>>> 883f177275fd7ecdac54a31c77ea89042855b1d9


def get_user_saved_tracks(sp):
    saved_results = sp.current_user_saved_tracks(limit=1)
    count = 0
    while count < saved_results['total']:
        results = sp.current_user_saved_tracks(limit=50,offset=count)
        count += 50
        saved_songs = save_songs(saved_results['items'])

def get_user_playlist_tracks(sp):
<<<<<<< HEAD
	username = sp.current_user()['id']
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
	 	if playlist['owner']['id'] == username:
	 		playlist_results = sp.user_playlist_tracks(username, playlist['id'],
                fields="total,items")
	 		count = 0
	 		while count < playlist_results['total']:
	 			playlist_results = sp.user_playlist_tracks(username, playlist['id'],limit=50,offset=count,fields="total, items")
	 			count += 50
	 			saved_songs = save_songs(playlist_results['items'])
	
=======
     playlists = sp.user_playlists(username)


>>>>>>> 883f177275fd7ecdac54a31c77ea89042855b1d9

# spotify:user:11800860


class SeedUserLibraryView(View):

<<<<<<< HEAD
	def get(self, request):
		user = User.objects.filter(pk=request.session['session_id'])
		if len(user) == 1:
			post_route = "https://accounts.spotify.com/api/token"
			callback = SPOTIPY_REDIRECT_URI
			grant_type = "authorization_code"
			pay_load = {"grant_type":grant_type, "code":request.session['spotify_code'], "redirect_uri":callback,"client_id":SPOTIPY_CLIENT_ID,"client_secret":SPOTIPY_CLIENT_SECRET}
			r = requests.post(post_route,data=pay_load)
			token = r.json()['access_token']
			request.session['user_token'] = token
			sp = spotipy.Spotify(auth=token)
			saved_tracks = get_user_saved_tracks(sp)
			playlist_tracks = get_user_playlist_tracks(sp)		
			return JsonResponse({"status": "Success"})
=======
    def get(self, request):
        user = User.objects.filter(pk=request.session['session_id'])
        if len(user) == 1:
            post_route = "https://accounts.spotify.com/api/token"
            callback = SPOTIPY_REDIRECT_URI
            grant_type = "authorization_code"
            pay_load = {"grant_type":grant_type, "code":request.session['spotify_code'], "redirect_uri":callback,"client_id":SPOTIPY_CLIENT_ID,"client_secret":SPOTIPY_CLIENT_SECRET}
            r = requests.post(post_route,data=pay_load)
            token = r.json()['access_token']
            request.session['user_token'] = token
            sp = spotipy.Spotify(auth=token)
            saved_tracks = get_user_saved_tracks(sp)
            playlist_tracks = get_user_playlist_tracks(sp)
            


        
        
            return JsonResponse({"status": "Success"})
>>>>>>> 883f177275fd7ecdac54a31c77ea89042855b1d9

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
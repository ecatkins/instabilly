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
	        print('successful user save')
	        return redirect("oauth")
	    else:
	        return render(request, 'spotify/home.html', {"login_form": UserForm(), "error": "Username already exists.", "registration_form": RegistrationForm()})


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
		x = oauth2.SpotifyOAuth(CLIENTID,CLIENTSECRET,"http://127.0.0.1:8000/callback",scope="user-library-read")
		url = x.get_authorize_url()
		return redirect(url)


class SyncView(View):
	template = "spotify/index.html"

	def get(self,request):
		code = request.GET.get('code')
		request.session['spotify_code'] = code
		return render(request, self.template)



class SeedPlaylistView(View):

	def get(self, request):
		user = User.objects.filter(pk=request.session['session_id'])
		if len(user) == 1:
			post_route = "https://accounts.spotify.com/api/token"
			callback = "http://127.0.0.1:8000/callback"
			grant_type = "authorization_code"
			pay_load = {"grant_type":grant_type, "code":request.session['spotify_code'], "redirect_uri":callback,"client_id":CLIENTID,"client_secret":CLIENTSECRET}
			r = requests.post(post_route,data=pay_load)
			token = r.json()['access_token']
			sp = spotipy.Spotify(auth=token)
			results = sp.current_user_saved_tracks(limit=1)
			count = 0
			while count < results['total']:
				results = sp.current_user_saved_tracks(limit=50,offset=count)
				count += 50
				for item in results['items']:
					try:
						test_song = Song.objects.filter(track_name=item['track']['name'])
						if len(test_song) == 0:
							song = Song(track_name=item['track']['name'], track_id=item['track']['id'], track_uri=item['track']['uri'], artist=item['track']['artists'][0]['name'], artist_id=item['track']['artists'][0]['id'], album=item['track']['album']['name'], album_id=item['track']['album']['id'], album_uri=item['track']['album']['uri'], spotify_popularity=item['track']['popularity'], preview_url=item['track']['preview_url'], image_300=item['track']['album']['images'][1]['url'], image_64=item['track']['album']['images'][2]['url'])
							song.save()
							print(song.track_name)
							usersong = UserSong(user=user[0], song=song)
							usersong.save()
							print("usersong successs")
					except:
						continue
			return JsonResponse({"status": "Success"})

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
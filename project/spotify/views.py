from django.shortcuts import render, redirect
from django.views.generic import View
import spotipy
from spotipy import oauth2
import spotipy.util as util
import requests
from secret import *





class IndexView(View):

	def get(self,request):
		x = oauth2.SpotifyOAuth(CLIENTID,CLIENTSECRET,"http://localhost:8000/callback",scope="user-library-read")
		url = x.get_authorize_url()

		return redirect(url)

class TestView(View):
	template = "spotify/index.html"

	def get(self,request):
		code = request.GET.get('code')
		post_route = "https://accounts.spotify.com/api/token"
		callback = "http://localhost:8000/callback"
		grant_type = "authorization_code"
		pay_load = {"grant_type":grant_type, "code":code, "redirect_uri":callback,"client_id":CLIENTID,"client_secret":CLIENTSECRET}

		r = requests.post(post_route,data=pay_load)
		# print(r.status_code)
		# print(r.content)
		token = r.json()['access_token']
		sp = spotipy.Spotify(auth=token)
		results = sp.current_user_saved_tracks(limit=1)
		print(results)
		count = 0
		# while count < results['total']:
		# 	results = sp.current_user_saved_tracks(limit=50,offset=count)
		# 	count += 50
		# 	for x in results['items']:
		# 		print(x['track']['name'])

		return render(request, self.template)
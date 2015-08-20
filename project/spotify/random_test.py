# import sys
# import spotipy
# import spotipy.util as util

# def show_tracks(results):
#     for i, item in enumerate(tracks['items']):
#         track = item['track']
#         print ("   {0} {1} {2}".format( i, track['artists'][0]['name'],
#             track['name']))


# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         username = sys.argv[1]
#     else:
#         print ("Whoops, need your username!")
#         print ("usage: python user_playlists.py [username]")
#         sys.exit()

#     token = util.prompt_for_user_token(username)

#     if token:
#         sp = spotipy.Spotify(auth=token)
#         print(sp.current_user()['id'])
#         print(dir(sp.current_user()))
#         playlists = sp.user_playlists(username)
#         for playlist in playlists['items']:
#             print(playlist['name'])
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 print
#                 print (playlist['name'])
#                 print ('  total tracks', playlist['tracks']['total'])
#                 results = sp.user_playlist(username, playlist['id'],
#                     fields="tracks,next")
#                 # print(results)
#                 tracks = results['tracks']
#                 show_tracks(tracks)
#                 while tracks['next']:
#                     tracks = sp.next(tracks)
#                     show_tracks(tracks)
#     else:
#         print ("Can't get token for", username)

import random
from sklearn.neighbors import KNeighborsClassifier
total_array = []
for x in range(1000):
    row = []
    for y in range(600):
        row.append(random.random())
    total_array.append(row)

X = total_array
print(len(X))
y = [random.random() for i in range(1000)]

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)
print(neigh.kneighbors([random.random() for i in range(600)],3))

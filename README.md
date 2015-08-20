# instasong
## App Summary

## Recommendation Engine
* User 0 at time 0 will have no friends to develop recommendations. Everything will have to be purely built off user's current spotify playlist and any preferences they might indicate in their profile.
* At the start we can probably use EchoNest to generate some random playlists/albums/songs based on these initial recommendations
* From there we can consider a number of ways to update recommendations...
    * Music based on their friends playlists/saved songs
    * People who they are not friends with on the site, but have similar music tastes
    * A like / dislike button on any recommendations that we provide them. This information would probably have to be stored in a database. If a song is marked positively / negatively, that increases / decreases the weighting on that particular artist and genre of music for that user (also could potentially be used as a weighting factor for people with similar tastes)
* Weighting / ranking system
    * Based on a combination of the previous three recommendation factors?
    * Score out of 100
    * Include a bias for new music
    * Then how do we ensure we are constantly serving new music to the user?

## Front End


#### General Resources
1. [Spotipy Docs] (http://spotipy.readthedocs.org/en/latest/#examples)
2. [Spotify Play Button Widget] (https://developer.spotify.com/technologies/widgets/spotify-play-button/)
3. [Echnoest Pyen] (https://github.com/plamere/pyen) *
4. [Echonest pyechonest] (https://github.com/echonest/pyechonest)
5. [Pitchfork Reviews API] (https://github.com/michalczaplinski/pitchfork)
5. [Markdown Cheatsheet] (https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
6. [KD Tree] (http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.html)

#### For migration issues
1. http://stackoverflow.com/questions/29689365/auth-user-error-with-django-1-8-and-syncdb-migrate
2. 

#### Scipy on server
http://mail.scipy.org/pipermail/scipy-user/2013-November/035171.html

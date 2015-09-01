import uuid
from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

class Song(models.Model):
    track_name = models.CharField(max_length=200)
    track_id = models.CharField(db_index=True, max_length=200)
    track_uri = models.CharField(max_length=200)
    artists = models.ForeignKey('Artist')
    artist_id = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    album_id = models.CharField(max_length=200)
    album_uri = models.CharField(max_length=200)
    spotify_popularity = models.IntegerField(default=0)
    preview_url = models.URLField()
    image_300 = models.URLField()
    image_64 = models.URLField()
    users = models.ManyToManyField(User, through='UserSong')
    artist = models.CharField(max_length=200)
    


class Genre(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through="UserGenre")


class UserGenre(models.Model):
    user = models.ForeignKey(User)
    genre = models.ForeignKey(Genre)
    proportion = models.FloatField()


class Artist(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
 
class UserActivationCode(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    activated = models.BooleanField(default=False)
    updated_genres = models.DateTimeField()
    active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

class FollowList(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    following = models.ManyToManyField(User, related_name='following')

class UserSong(models.Model):
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    uploaded_at = models.DateField()
    synced_at = models.DateField(auto_now_add=True)

class ArtistRating(models.Model):
    user = models.ForeignKey(User)
    artist = models.ForeignKey(Artist)
    score = models.DecimalField(max_digits=6, decimal_places=4,default=0.5)


class Post(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(UserSong)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



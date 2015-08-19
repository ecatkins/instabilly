from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    track_name = models.CharField(max_length=200)
    track_id = models.CharField(db_index=True, max_length=200)
    track_uri = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    album_id = models.CharField(max_length=200)
    album_uri = models.CharField(max_length=200)
    spotify_popularity = models.IntegerField(default=0)
    preview_url = models.URLField()
    image_300 = models.URLField()
    image_64 = models.URLField()
    users = models.ManyToManyField(User, through='UserSong')


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    is_real = models.BooleanField()
    x_coord = models.DecimalField(max_digits=5, decimal_places=3)
    y_coord = models.DecimalField(max_digits=5, decimal_places=3)


class FollowList(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    following = models.ManyToManyField(User, related_name='following')


class UserSong(models.Model):
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    uploaded_at = models.DateField(auto_now_add=True)
    synced_at = models.DateField(auto_now_add=True)

###Need the table for Users and non-owned songs


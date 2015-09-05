# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_auto_20150820_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ArtistRating',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('score', models.DecimalField(default=0.5, decimal_places=4, max_digits=6)),
                ('artist', models.ForeignKey(to='spotify.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='FollowList',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NearestNeigh',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('track_name', models.CharField(max_length=200)),
                ('track_id', models.CharField(db_index=True, max_length=200)),
                ('track_uri', models.CharField(max_length=200)),
                ('artist_id', models.CharField(max_length=200)),
                ('album', models.CharField(max_length=200)),
                ('album_id', models.CharField(max_length=200)),
                ('album_uri', models.CharField(max_length=200)),
                ('spotify_popularity', models.IntegerField(default=0)),
                ('preview_url', models.URLField()),
                ('image_300', models.URLField()),
                ('image_64', models.URLField()),
                ('artists', models.ForeignKey(to='spotify.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserActivationCode',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('proportion', models.FloatField()),
                ('genre', models.ForeignKey(to='spotify.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('updated_genres', models.DateTimeField()),
                ('verified', models.BooleanField(default=False)),
                ('neighs', models.ManyToManyField(through='spotify.NearestNeigh', to=settings.AUTH_USER_MODEL, related_name='neighs')),
            ],
        ),
        migrations.CreateModel(
            name='UserSong',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('uploaded_at', models.DateField()),
                ('synced_at', models.DateField(auto_now_add=True)),
                ('song', models.ForeignKey(to='spotify.Song')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usergenre',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='song',
            name='users',
            field=models.ManyToManyField(through='spotify.UserSong', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='song',
            field=models.ForeignKey(to='spotify.UserSong'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nearestneigh',
            name='neighbor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nearestneigh',
            name='user',
            field=models.ForeignKey(to='spotify.UserProfile'),
        ),
        migrations.AddField(
            model_name='genre',
            name='users',
            field=models.ManyToManyField(through='spotify.UserGenre', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followlist',
            name='following',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='following'),
        ),
        migrations.AddField(
            model_name='artistrating',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(to='spotify.Genre'),
        ),
    ]

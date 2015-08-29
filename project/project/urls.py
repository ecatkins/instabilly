from django.conf.urls import include, url
from django.contrib import admin
from spotify.views import HomeView, OauthView, SyncView, RegistrationView, LoginView, SeedUserLibraryView, LogoutView, GetFollowingView, FollowView, UnfollowView, SearchView, TrackURIView, CreatePostView, EngineView, PlaylistView, GetMiniFeedView, RatingView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^oauth$', OauthView.as_view(), name="oauth"),
    url(r'^registration$', RegistrationView.as_view(), name="registration"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
    url(r'^callback', SyncView.as_view(), name="sync"),
    url(r'^seed$', SeedUserLibraryView.as_view(), name="seed"),
    url(r'^getfollowing$', GetFollowingView.as_view(), name="getfollowing"),
    url(r'^follow$', FollowView.as_view(), name="follow"),
    url(r'^unfollow$', UnfollowView.as_view(), name="unfollow"),
    url(r'^engine$', EngineView.as_view(), name="engine"),
    url(r'^playlist$', PlaylistView.as_view(), name="playlist"),
    url(r'^rating$', RatingView.as_view(), name="rating"),
    url(r'^saveplaylist$',SavePlaylistView.as_view(),name="save_playlist")
    url(r'^search$', SearchView.as_view(), name="search"),
    url(r'^track_uri$', TrackURIView.as_view(), name="track_uri"),
    url(r'^create_post$', CreatePostView.as_view(), name="create_post"),
    url(r'^get_minifeed$', GetMiniFeedView.as_view(), name="get_minifeed"),
    url(r'^admin/', include(admin.site.urls))
]

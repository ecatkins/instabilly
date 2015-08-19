from django.conf.urls import include, url
from django.contrib import admin
from spotify.views import HomeView, IndexView, TestView, SyncView, RegistrationView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^oauth$', OauthView.as_view(), name="oauth"),
    url(r'^registration$', RegistrationView.as_view(), name="registration"),
    url(r'^callback', SyncView.as_view(), name="sync"),
    url(r'^seed', SeedPlaylistView.as_view(), name="seed"),
    url(r'^admin/', include(admin.site.urls))
]

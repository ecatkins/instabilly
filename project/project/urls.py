from django.conf.urls import include, url
from django.contrib import admin
from spotify.views import IndexView, TestView, SyncView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name = "index"),
    url(r'^callback', TestView.as_view(), name = "test"),
    url(r'^sync', SyncView.as_view(), name = "sync")
]

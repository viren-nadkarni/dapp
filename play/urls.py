from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^app/(.*)/$', views.app, name='app'),
    url(r'^results/$', views.results, name='results'),
]

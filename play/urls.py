from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^results/(.*)/$', views.app, name='app'),
    url(r'^results/$', views.results, name='results'),
]

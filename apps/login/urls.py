from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$' , views.register_process),
    url(r'^login_process$' , views.login_process),
    url(r'^quotes$' , views.quotes),
    url(r'^quotes/(?P<id>\d+)$' , views.quotes),
    url(r'^logout$', views.logout),
    url(r'^add_my_quote_process$', views.add_my_quote_process),
    url(r'^add_my_fave/(?P<id>\d+)$', views.add_my_fave),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^remove_my_fave/(?P<id>\d+)$', views.remove_my_fave),
]
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$' , views.register_process),
    url(r'^login_process$' , views.login_process),
    url(r'^success$' , views.success),
    url(r'^success/(?P<id>\d+)$' , views.success),
    url(r'^logout$', views.logout),
    url(r'^add_book_review/(?P<id>\d+)$' , views.add_book_review),
    url(r'^add_book_review_process/(?P<id>\d+)$' , views.add_book_review_process),
    url(r'^add_review_each_book_process/(?P<id>\d+)$', views.add_review_each_book_process),
    url(r'^each_book/(?P<id>\d+)$', views.each_book),
    url(r'^user_info/(?P<id>\d+)$', views.user_info),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review),
]
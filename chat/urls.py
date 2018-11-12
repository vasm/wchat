from django.conf.urls import url
# from django.conf.urls import include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registered/$', views.reg_succeeded, name='registered'),
    url(r'^password_reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done,
        name='password_reset_done'),

    # JSON methods:
    url(r'^api/messages_from/(?P<message_id>[0-9]+)/$',
        views.messages_from,
        name='messages_from'),
    url(r'^api/send/$', views.send, name='send'),
    url(r'^api/contacts/$', views.contacts, name='contacts'),
]

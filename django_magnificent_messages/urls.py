# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'django_magnificent_messages'
urlpatterns = [
    url(
        regex="^Message/~create/$",
        view=views.MessageCreateView.as_view(),
        name='Message_create',
    ),
    url(
        regex="^Message/(?P<pk>\d+)/~delete/$",
        view=views.MessageDeleteView.as_view(),
        name='Message_delete',
    ),
    url(
        regex="^Message/(?P<pk>\d+)/$",
        view=views.MessageDetailView.as_view(),
        name='Message_detail',
    ),
    url(
        regex="^Message/(?P<pk>\d+)/~update/$",
        view=views.MessageUpdateView.as_view(),
        name='Message_update',
    ),
    url(
        regex="^Message/$",
        view=views.MessageListView.as_view(),
        name='Message_list',
    ),
	]

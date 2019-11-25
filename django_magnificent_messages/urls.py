"""
URLs for django_magnificent_messages
"""
from django.urls import path

from . import views

app_name = 'django_magnificent_messages'
urlpatterns = [
    path(
        "text/create",
        views.MessageCreateView.as_view(),
        name='Message_create',
    ),
    path(
        "text/<int:pk>/delete",
        views.MessageDeleteView.as_view(),
        name='Message_delete',
    ),
    path(
        "text/<int:pk>",
        views.MessageDetailView.as_view(),
        name='Message_detail',
    ),
    path(
        "text/<int:pk>/update",
        views.MessageUpdateView.as_view(),
        name='Message_update',
    ),
    path(
        "text",
        views.MessageListView.as_view(),
        name='Message_list',
    ),
]

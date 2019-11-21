# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel

from .conf import settings, MessageConfig

config = MessageConfig()


class Message(TimeStampedModel):
    level = models.IntegerField()
    persistent = models.BooleanField()

    subject = models.TextField(blank=True)
    message = models.TextField(blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="outbox")
    user_generated = models.BooleanField(default=False)

    reply_to = models.ForeignKey('django_magnificent_messages.Message', on_delete=models.PROTECT,
                                 related_name="replies")
    send_to_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="inbox")
    send_to_group = models.ManyToManyField('auth.Group', related_name="inbox")
    



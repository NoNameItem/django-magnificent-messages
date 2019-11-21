from django.db import models

from django_magnificent_messages.fields import JSONField


class JSONFieldTestModel(models.Model):
    field = JSONField()

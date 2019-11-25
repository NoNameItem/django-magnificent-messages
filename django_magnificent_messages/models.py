"""
Models for django_magnificent_messages
"""
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from django_magnificent_messages import constants
from django_magnificent_messages.fields import JSONField
from .conf import settings
from .storage.message_storage.db_signals import message_archived, message_read, message_unarchived, message_unread


class MessageManager(models.Manager):
    pass


class Message(TimeStampedModel):
    """
    Main model for app.

    Stores one record for every text in system
    """
    level = models.IntegerField()

    subject = models.TextField(blank=True)
    text = models.TextField()
    extra = JSONField(blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="outbox")
    user_generated = models.BooleanField()

    reply_to = models.ForeignKey('django_magnificent_messages.Message', on_delete=models.PROTECT,
                                 related_name="replies", null=True)
    sent_to_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="messages",
                                           db_table="mm_message_sent_to_user")
    sent_to_group = models.ManyToManyField('auth.Group', related_name="messages", db_table="mm_message_sent_to_group")
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="read_messages",
                                     db_table="mm_message_read_by_user")
    archived_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="archived_messages",
                                         db_table="mm_message_archived_by_user")

    objects = models.Manager()

    class Meta:
        db_table = "mm_message"
        default_permissions = ()
        permissions = (
            ("send_message", "Send text"),
            ("view_all_message", "View all text"),
            ("delete_any_message", "Delete any text"),
        )
        ordering = ("created",)

    def archive(self, user):
        self.archived_by.add(user)
        message_archived.send(sender=self.__class__, message=self, user=user)

    def unarchive(self, user):
        self.archived_by.remove(user)
        message_unarchived.send(sender=self.__class__, message=self, user=user)

    def mark_read(self, user):
        self.read_by.add(user)
        message_read.send(sender=self.__class__, message=self, user=user)

    def mark_unread(self, user):
        self.read_by.remove(user)
        message_unread.send(sender=self.__class__, message=self, user=user)


class Inbox(models.Model):
    """
    Inbox model.

    Represents user inbox. Stores time, when inbox was checked last and provides methods for getting messages in inbox.

    It's possible that in future django-magnificent-messages will support multiple inboxes, so we use ForeignKey
    instead of OneToOneField and Inbox has field ``name`` with default="Inbox"
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="inboxes")
    name = models.CharField(max_length=200, default="Inbox")
    main = models.BooleanField(default=False)
    desc = models.TextField(blank=True)
    last_checked = models.DateTimeField(default=constants.MIN_DATETIME)

    @property
    def all(self) -> QuerySet:
        return self._all()

    @property
    def all_count(self) -> int:
        return self._all(set_last_checked=False).count()

    @property
    def read(self) -> QuerySet:
        return self._read(set_last_checked=False)

    @property
    def read_count(self) -> int:
        return self._read(set_last_checked=False).count()

    @property
    def unread(self) -> QuerySet:
        return self._unread()

    @property
    def unread_count(self) -> int:
        return self._unread(set_last_checked=False).count()

    @property
    def archived(self) -> QuerySet:
        return self._get_messages(set_last_checked=False, archived=True)

    @property
    def archived_count(self) -> int:
        return self.archived.count()

    @property
    def new(self):
        return self._all().filter(created__gt=self.last_checked)

    @property
    def new_count(self):
        return self._all(set_last_checked=False).filter(created__gt=self.last_checked)

    class Meta:
        db_table = "mm_inbox"
        unique_together = (
            ("user", "name")
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Preventing more than one main inbox
        """
        if self.main and Inbox.objects.filter(user=self.user, main=True):
            raise ValidationError(
                _("User %(user)s already has main inbox"),
                code="invalid",
                params={
                    "user": str(self.user)
                }
            )
        super(Inbox, self).save(force_insert, force_update, using, update_fields)

    def _get_messages(self, set_last_checked: bool = True, archived: bool = False, q: Q = Q()) -> QuerySet:
        """
        Get messages in this inbox and filter them with q.

        Get messages sent to user directly or through some of user groups. Excepts archived messages

        Uses two queries to avoid duplication of messages sent to user directly and through the groups, or through
        two and more groups. Can't use distinct() because Oracle does not support distinct on NCLOB fields and
        Message model has such fields (subject, text and extra)

        **You should not use this method directly. Use properties instead**

        :param set_last_checked: should method update last_checked?
        :param archived: If False (default) - exclude archived. If true - notifications_show only archived
        :param q: Q object to filter messages
        :return:
        """
        # Update last checked
        if set_last_checked:
            self.last_checked = timezone.now()
            self.save()

        # Get distinct messages pks
        to_user_q = Q(sent_to_users=self.user)
        if hasattr(self.user, "groups") and hasattr(self.user.groups, "all") and callable(self.user.groups.all):
            q = q | Q(sent_to_group__group_id__in=list(self.user.groups.all()))
        message_pks = Message.objects.filter(to_user_q).values("id").distinct()

        # Get messages with pk in messsage_pks
        messages = Message.objects.filter(pk__in=message_pks)

        if archived:
            messages = messages.filter(archived_by=self.user)
        else:
            messages = messages.exclude(archived_by=self.user)

        messages = messages.filter(q)

        return messages

    def _all(self, set_last_checked: bool = True) -> QuerySet:
        """
        Returns all messages in inbox except archived
        """
        return self._get_messages(set_last_checked)

    def _read(self, set_last_checked: bool = True) -> QuerySet:
        return self._get_messages(set_last_checked, q=Q(pk__in=self.read.values("pk")))

    def _unread(self, set_last_checked: bool = True) -> QuerySet:
        return self._get_messages(set_last_checked, q=~Q(pk__in=self.read.values("pk")))

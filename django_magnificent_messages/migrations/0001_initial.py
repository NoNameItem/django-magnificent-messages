# Generated by Django 2.2.4 on 2019-11-27 15:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_magnificent_messages.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('level', models.IntegerField()),
                ('subject', models.TextField(blank=True, null=True)),
                ('text', models.TextField()),
                ('extra', django_magnificent_messages.fields.JSONField(blank=True, null=True)),
                ('user_generated', models.BooleanField()),
                ('archived_by', models.ManyToManyField(db_table='mm_message_archived_by_user', related_name='archived_messages', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outbox', to=settings.AUTH_USER_MODEL)),
                ('read_by', models.ManyToManyField(db_table='mm_message_read_by_user', related_name='read_messages', to=settings.AUTH_USER_MODEL)),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='django_magnificent_messages.Message')),
                ('sent_to_groups', models.ManyToManyField(db_table='mm_message_sent_to_group', related_name='messages', to='auth.Group')),
                ('sent_to_users', models.ManyToManyField(db_table='mm_message_sent_to_user', related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mm_message',
                'ordering': ('created',),
                'permissions': (('send_message', 'Send text'), ('view_all_message', 'View all text'), ('delete_any_message', 'Delete any text')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Inbox', max_length=200)),
                ('main', models.BooleanField(default=False)),
                ('desc', models.TextField(blank=True)),
                ('last_checked', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0))),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inboxes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mm_inbox',
                'unique_together': {('user', 'name')},
            },
        ),
    ]

from typing import Iterable

from django.http import HttpRequest

from django_magnificent_messages.messages import MessageFailure
from .backend import MessageBackend
from . import constants

__all__ = (
    'add', 'secondary', 'primary', 'info', 'success', 'warning', 'error',
)


def add(request: HttpRequest,
        level: int,
        text: str,
        subject: str = None,
        extra: object = None,
        to_users_pk: Iterable = tuple(),
        to_groups_pk: Iterable = tuple(),
        fail_silently: bool = False) -> None:
    """
    Attempt to notifications_add a notification to the request using the 'django_magnificent_messages' app.
    """
    try:
        backend = request.dmm_backend  # type: MessageBackend
    except AttributeError:
        if not isinstance(request, HttpRequest):
            raise TypeError(
                "add_message() argument must be an HttpRequest object, not "
                "'%s'." % request.__class__.__name__
            )
        if not fail_silently:
            raise MessageFailure(
                'You cannot notifications_add messages without installing '
                'django_magnificent_messages.middleware.MessageMiddleware'
            )
    else:
        return backend.send_message(level, text, subject, extra, to_users_pk, to_groups_pk, False)


def secondary(request: HttpRequest,
              text: str,
              subject: str = None,
              extra: object = None,
              to_users_pk: Iterable = tuple(),
              to_groups_pk: Iterable = tuple(),
              fail_silently: bool = False) -> None:
    """Add a message with the ``SECONDARY`` level."""
    add(request, constants.SECONDARY, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)


def primary(request: HttpRequest,
            text: str,
            subject: str = None,
            extra: object = None,
            to_users_pk: Iterable = tuple(),
            to_groups_pk: Iterable = tuple(),
            fail_silently: bool = False) -> None:
    """Add a message with the ``PRIMARY`` level."""
    add(request, constants.PRIMARY, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)


def info(request: HttpRequest,
         text: str,
         subject: str = None,
         extra: object = None,
         to_users_pk: Iterable = tuple(),
         to_groups_pk: Iterable = tuple(),
         fail_silently: bool = False) -> None:
    """Add a message with the ``INFO`` level."""
    add(request, constants.INFO, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)


def success(request: HttpRequest,
            text: str,
            subject: str = None,
            extra: object = None,
            to_users_pk: Iterable = tuple(),
            to_groups_pk: Iterable = tuple(),
            fail_silently: bool = False) -> None:
    """Add a message with the ``SUCCESS`` level."""
    add(request, constants.SUCCESS, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)


def warning(request: HttpRequest,
            text: str,
            subject: str = None,
            extra: object = None,
            to_users_pk: Iterable = tuple(),
            to_groups_pk: Iterable = tuple(),
            fail_silently: bool = False) -> None:
    """Add a message with the ``WARNING`` level."""
    add(request, constants.WARNING, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)


def error(request: HttpRequest,
          text: str,
          subject: str = None,
          extra: object = None,
          to_users_pk: Iterable = tuple(),
          to_groups_pk: Iterable = tuple(),
          fail_silently: bool = False) -> None:
    """Add a message with the ``ERROR`` level."""
    add(request, constants.ERROR, text, subject, extra, to_users_pk, to_groups_pk, fail_silently=fail_silently)

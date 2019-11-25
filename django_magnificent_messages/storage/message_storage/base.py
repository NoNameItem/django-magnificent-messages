from typing import Iterable

from django_magnificent_messages.storage.base import BaseStorage, Message


class BaseMessageStorage(BaseStorage):
    """
    This is the base message storage.

    We divide messages into following types:
      * All messages
      * Read messages
      * Unread messages
      * Archived messages
      * New messages (messages received since last check)

    Storage should provide methods for getting iterable object of every of this types of messages and methods for
    getting count of messages of each type. This methods wrapped in properties defined in this class.

    Storage should also provide method for saving new message for users or groups.

    **This is not a complete class; to be a usable storage, it must be subclassed and all unimplemented methods
    overridden.**
    """

    # Storage API

    @property
    def all(self) -> Iterable:
        return self._get_all_messages_iter()

    @property
    def read(self) -> Iterable:
        return self._get_read_messages_iter()

    @property
    def unread(self) -> Iterable:
        return self._get_unread_messages_iter()

    @property
    def archived(self) -> Iterable:
        return self._get_archived_messages_iter()

    @property
    def new(self) -> Iterable:
        return self._get_new_messages_iter()

    @property
    def all_count(self) -> int:
        return self._get_all_messages_count()

    @property
    def read_count(self) -> int:
        return self._get_read_messages_count()

    @property
    def unread_count(self) -> int:
        return self._get_unread_messages_count()

    @property
    def archived_count(self) -> int:
        return self._get_archived_messages_count()

    @property
    def new_count(self) -> int:
        return self._get_new_messages_count()

    def send_message(self,
                     level: int,
                     text: str,
                     subject: str = None,
                     extra: object = None,
                     to_users_pk: Iterable = tuple(),
                     to_groups_pk: Iterable = tuple(),
                     user_generated: bool = True,
                     reply_to_pk=None) -> None:
        """
        Send message.

        Checks message level and that recipient list is not empty. Construct ``Message`` instance and pass it
        into ``_save_message`` method if all checks passed.
        """
        message = self._construct(level, text, subject, extra)
        if message is not None and (to_users_pk or to_groups_pk):
            if user_generated \
               and hasattr(self.request, 'user') \
               and getattr(self.request.user, "is_authenticated", False):
                sender_pk = getattr(self.request.user, "pk")
            else:
                sender_pk = None

            self._save_message(message, to_users_pk, to_groups_pk, user_generated, reply_to_pk)

    # Storage internal methods to implement in subclass

    def _get_all_messages_iter(self) -> Iterable:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_all_messages_iter() method')

    def _get_read_messages_iter(self) -> Iterable:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_read_messages_iter() method')

    def _get_unread_messages_iter(self) -> Iterable:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_unread_messages_iter() method')

    def _get_archived_messages_iter(self) -> Iterable:
        """This method must be implemented by a subclass."""
        raise NotImplementedError(
            'subclasses of BaseMessageStorage must provide a _get_archived_messages_iter() method'
        )

    def _get_new_messages_iter(self) -> Iterable:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_new_messages_iter() method')

    def _get_all_messages_count(self) -> int:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_all_messages_count() method')

    def _get_read_messages_count(self) -> int:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_read_messages_count() method')

    def _get_unread_messages_count(self) -> int:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_unread_messages_count() method')

    def _get_archived_messages_count(self) -> int:
        """This method must be implemented by a subclass."""
        raise NotImplementedError(
            'subclasses of BaseMessageStorage must provide a _get_archived_messages_count() method'
        )

    def _get_new_messages_count(self) -> int:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _get_new_messages_count() method')

    def _save_message(self,
                      message: Message,
                      author_pk,
                      to_users_pk: Iterable,
                      to_groups_pk: Iterable,
                      user_generated: bool,
                      reply_to_pk) -> None:
        """This method must be implemented by a subclass."""
        raise NotImplementedError('subclasses of BaseMessageStorage must provide a _save_message() method')

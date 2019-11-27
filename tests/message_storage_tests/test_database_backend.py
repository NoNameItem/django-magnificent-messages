from django.test import TestCase

from django_magnificent_messages.storage.message_storage.db import DatabaseStorage
from tests.message_storage_tests.base import BaseMessageStorageTestCases


class DatabaseStorageExistingTestCase(BaseMessageStorageTestCases.ExistingMessagesTestCase):
    STORAGE = DatabaseStorage

class DatabaseStorageClearTestCase(BaseMessageStorageTestCases.ClearTestCase):
    STORAGE = DatabaseStorage
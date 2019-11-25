"""
Constants and defaults values
"""
import datetime

from django.utils import timezone

SECONDARY = 10
PRIMARY = 20
INFO = 30
SUCCESS = 40
WARNING = 50
ERROR = 60

DEFAULT_TAGS = {
    SECONDARY: 'secondary',
    PRIMARY: 'primary',
    INFO: 'info',
    SUCCESS: 'success',
    WARNING: 'warning',
    ERROR: 'error',
}

DEFAULT_LEVELS = {
    'SECONDARY': SECONDARY,
    'PRIMARY': PRIMARY,
    'INFO': INFO,
    'SUCCESS': SUCCESS,
    'WARNING': WARNING,
    'ERROR': ERROR,
}

MESSAGE_FILES_UPLOAD_TO = "django_magnificent_messages/message_files"
MESSAGE_DB_MODEL = "django_magnificent_messages.Message"

DEFAULT_NOTIFICATION_STORAGE = "django_magnificent_messages.notification_storage.fallback.SessionStorage"
DEFAULT_MESSAGE_STORAGE = "django_magnificent_messages.message_storage.db.DatabaseStorage"

MIN_DATETIME = datetime.datetime.min

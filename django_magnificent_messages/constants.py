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

from django.conf import settings
from appconf import AppConf

from django_magnificent_messages import constants


class MessageConfig(AppConf):
    LEVELS = constants.DEFAULT_LEVELS
    LEVEL_TAGS = constants.DEFAULT_TAGS
    MINIMAL_LEVEL = constants.INFO
    MESSAGE_FILES_UPLOAD_TO = constants.MESSAGE_FILES_UPLOAD_TO
    MESSAGE_DB_MODEL = constants.MESSAGE_DB_MODEL

    class Meta:
        prefix = 'dmm'

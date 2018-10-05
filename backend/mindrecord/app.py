import os
import logging
from pymongo import MongoClient

from mindrecord.utils import BaseConfig


__all__ = ['config', 'db']

_logger = logging.getLogger(__name__)


# Default configuration
class Config(BaseConfig):
    DEBUG = True

    # Tests config (business logic)
    TESTS_CONFIG_PATTERN = 'D:\\Tests\\*\\*.mindrecord.json'
    TESTS_RESULTS_DIR = 'D:\\TestsResults\\'
    TESTS_RESULTS_RAW_FILE = 'raw.json'
    TESTS_RESULTS_FILE = 'results.json'
    TESTS_PROCESSING_LOG = 'output.log'
    TESTS_PROCESSING_ERROR_LOG = 'error.log'

    # Auth and security settings
    AUTH_ALLOW_ANONYMOUS = True
    AUTH_BCRYPT_ROUNDS = 10

    JWT_SECRET = 'CHANGE_ME'
    JWT_ALGORITHM = 'HS256'
    JWT_ISSUER = 'MindRecordAPIServer'
    JWT_ROLE_CLAIM = 'role'
    JWT_USER_ID_CLAIM = 'sub'
    JWT_KIND_CLAIM = 'kind'
    JWT_ACCESS_EXPIRATION_SECONDS = 60 * 60 * 48  # 48-hours token
    JWT_REFRESH_EXPIRATION_SECONDS = 60 * 60 * 24 * 30  # 30-days token
    JWT_EMAIL_CONFIRMATION_SECONDS = 60 * 60 * 24 * 30  # 30-days token

    # Database settings
    MONGO_DB_PATH = 'mongodb://localhost:27017/'
    MONGO_DB_NAME = 'mindrecord'

    SMTP_HOST = None
    SMTP_PORT = None
    SMTP_USERNAME = None
    SMTP_PASSWORD = None
    SMTP_SENDER_EMAIL = None


# Basic configuration
config = Config()

# Load configuration
_cfg_path = os.environ.get('MINDRECORD_CONFIG', None)
if _cfg_path:
    _logger.debug('Loading configuration: {0}'.format(_cfg_path))
    config.update(BaseConfig.from_file(_cfg_path))

# Database connection
_logger.debug('Connecting to database: {0}'.format(config.MONGO_DB_PATH))
_client = MongoClient(config.MONGO_DB_PATH)
db = _client[config.MONGO_DB_NAME]

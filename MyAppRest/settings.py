import os


def gcloud_secret(key, version):
    from google.cloud import secretmanager

    gcp_proj_id = os.environ.get('GCP_PROJECT_ID')
    client = secretmanager.SecretManagerServiceClient()

    name = client.secret_version_path(gcp_proj_id, key, version)
    return client.access_secret_version(name).payload.data.decode('UTF-8')


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    JWT_HEADER_TYPE = 'Token'
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    if os.environ.get('GCP_PROJECT_ID'):
        SQLALCHEMY_DATABASE_URI = gcloud_secret('MyAppRest_DB_URL', '1')
        SECRET_KEY = gcloud_secret('MyAppRest_SECRET_KEY', '1')
        SENDGRID_EMAIL = "alerts.chime.menu"

class DevConfig(Config):
    """Development configuration."""

    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'serviceclient')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5433)
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DB', 'chimedb')

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/' \
                              f'{POSTGRES_DATABASE}'

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_DB = os.environ.get('REDIS_DB', 0)
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_FOODIE_VERIFICATION_MSID = os.environ.get('TWILIO_FOODIE_VERIFICATION_MSID')
    TWILIO_PHONE_NUM = os.environ.get('TWILIO_PHONE_NUM')

    STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
    STRIPE_PI_WEBHOOK_SECRET = os.environ.get('STRIPE_PI_WEBHOOK_SECRET')

from sources.infrastructure import configuration
from sources.infrastructure.django import core


BASE_DIR = configuration.base_dir

DEBUG = configuration.debug

INSTALLED_APPS = core.module, "django_extensions"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": configuration.db_name,
        "USER": configuration.db_user,
        "PASSWORD": configuration.db_password,
        "HOST": configuration.db_host,
        "PORT": configuration.db_port,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECRET_KEY = configuration.secret_key

TIME_ZONE = configuration.time_zone

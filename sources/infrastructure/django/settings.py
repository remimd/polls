from sources.infrastructure import configuration
from sources.infrastructure.command import module as command_module
from sources.infrastructure.orm import module as orm_module


DEBUG = configuration.debug

INSTALLED_APPS = (
    command_module,
    orm_module,
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_extensions",
    "phonenumber_field",
)

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

# User Model
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = "orm.UserORM"

# Phone number config
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"

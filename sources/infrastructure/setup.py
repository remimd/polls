import os


def setup_project():
    setup_repositories()
    setup_django()


def setup_repositories():
    # Import here the repositories you want to use.
    from .adapters.polls.repositories import PollRepository  # noqa


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "sources.infrastructure.django.settings",
    )

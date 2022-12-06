from django.core.asgi import get_asgi_application

from sources.infrastructure.setup import setup_django


setup_django()

application = get_asgi_application()

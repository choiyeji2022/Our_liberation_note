import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Our_Liberation_Note.settings")

application = get_asgi_application()

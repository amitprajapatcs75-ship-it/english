"""
ASGI config for LSC project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from middleware.socker_auth import JWTAuthMiddlewareStack
from django.core.asgi import get_asgi_application
from users.routers import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})

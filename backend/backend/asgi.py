import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Setup Django before importing anything that depends on settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django_application = get_asgi_application()

# Now you can import other modules
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from files.routing import websocket_urlpatterns  # Импортируем маршруты WebSocket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back_file_server.settings")  # myproject - замените на имя вашего проекта

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)
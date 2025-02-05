from django.urls import re_path
from .consumers import JSONFileConsumer

websocket_urlpatterns = [
    re_path(r"ws/json-updates/$", JSONFileConsumer.as_asgi()),
]
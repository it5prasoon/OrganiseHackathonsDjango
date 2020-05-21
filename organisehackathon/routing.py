from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from main.consumers import EchoConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", EchoConsumer),
    ])
})
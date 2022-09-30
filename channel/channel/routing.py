# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.urls import path

# application = ProtocolTypeRouter({
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#                 ...
#             ])
#         ),
#     ),
# })

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/redis/', consumers.Consumers.as_asgi())
]
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import my_quiz_app.python_django.games.routing  # Import routing WebSocket z aplikacji `games`

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_quiz_app.python_django.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            my_quiz_app.python_django.games.routing.websocket_urlpatterns  # Użycie routing WebSocket z aplikacji `games`
        )
    ),
})

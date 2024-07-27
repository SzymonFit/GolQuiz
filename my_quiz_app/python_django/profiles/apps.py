# profiles/apps.py
from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_quiz_app.python_django.profiles'

    def ready(self):
        import my_quiz_app.python_django.profiles.signals

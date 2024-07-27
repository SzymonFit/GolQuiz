# profiles/management/commands/create_missing_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_quiz_app.python_django.profiles.models import UserProfile

class Command(BaseCommand):
    help = 'Create missing user profiles for existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created missing profiles'))

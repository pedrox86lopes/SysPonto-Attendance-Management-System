from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='pedrox86').exists():
            User.objects.create_superuser('pedrox86', 'pedrox86@example.com', 'password123')
            self.stdout.write('Superuser created successfully')
        else:
            self.stdout.write('Superuser already exists')
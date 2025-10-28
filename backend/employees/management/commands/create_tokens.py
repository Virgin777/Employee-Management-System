from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from employees.models import Employee


class Command(BaseCommand):
    help = 'Create authentication tokens for all existing users'

    def handle(self, *args, **options):
        users_without_tokens = Employee.objects.filter(auth_token__isnull=True)
        
        created_count = 0
        for user in users_without_tokens:
            Token.objects.create(user=user)
            created_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} tokens for existing users'
            )
        )

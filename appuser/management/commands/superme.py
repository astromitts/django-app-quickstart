from django.core.management.base import BaseCommand
from appuser.models import AppUser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            '-e',
            type=str,
            help='Email of user to make super user',
        )

    def handle(self, *args, **options):
        me = AppUser.objects.get(user__email=options['email'])
        me.user.is_staff = True
        me.user.is_superuser = True
        me.user.save()

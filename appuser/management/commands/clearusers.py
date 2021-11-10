from django.core.management.base import BaseCommand
from appuser.models import AppUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        for appuser in AppUser.objects.all():
            appuser.user.delete()
            appuser.delete()

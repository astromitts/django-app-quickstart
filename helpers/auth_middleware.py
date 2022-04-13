from django.conf import settings
from namer.utils import save_anonymous_user


def anonymous_user(get_response):
    def middleware(request):
        can_have_anonymous_user = settings.APPUSER_SETTINGS['allow_anonymous_users'] and\
            settings.APPUSER_SETTINGS['anonymous_users']['bypass_login']
        if can_have_anonymous_user and not request.user.is_authenticated:
            save_anonymous_user(request)
        response = get_response(request)
        return response

    return middleware

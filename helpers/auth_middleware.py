from django.conf import settings
from django.urls import resolve

from namer.utils import save_anonymous_user


def anonymous_user(get_response):
    def middleware(request):
        resolved_url = resolve(request.path)
        create_user_exempt_paths = [
            'login',
            'logout',
            'register'
        ]
        create_anonymous_user_path = resolved_url.url_name not in create_user_exempt_paths
        can_have_anonymous_user = settings.ALLOW_ANONYMOUS_USERS and create_anonymous_user_path
        if can_have_anonymous_user and not request.user.is_authenticated:
            save_anonymous_user(request)
        response = get_response(request)
        return response

    return middleware

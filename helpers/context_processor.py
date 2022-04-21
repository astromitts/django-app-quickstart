from django.conf import settings
from helpers.models import FeatureFlag


def context_processor(request):
    feature_flags = FeatureFlag.objects.all()
    flags = {}
    for flag in feature_flags:
        if flag.has_users:
            if request.user in flag.users.all():
                flags[flag.title] = flag.value == 1
            else:
                flags[flag.title] = False
        else:
            flags[flag.title] = flag.value == 1
    if request.user.is_authenticated:
        is_anonymous = request.user.appuser.is_anonymous
    else:
        is_anonymous = True
    return {
        'flags': flags,
        'templates': {
            'display_username': settings.DISPLAY_USER_NAME and not is_anonymous,
            'display_logout': request.user.is_authenticated and not is_anonymous,
            'display_create_account': request.user.is_authenticated and is_anonymous,
        }
    }

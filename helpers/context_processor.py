from django.conf import settings
from django.urls import reverse

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

    allow_account_conversion = settings.ALLOW_CONVERT_TO_PERMANENT_USER

    if is_anonymous and not settings.ALLOW_ANONYMOUS_USERS:
        banner_brand_nav = reverse(settings.UNAUTHENTICATED_LANDING_PAGE)
    else:
        banner_brand_nav = reverse(settings.AUTHENTICATED_LANDING_PAGE)

    return {
        'flags': flags,
        'templates': {
            'banner_brand_nav': banner_brand_nav,
            'display_username': settings.DISPLAY_USER_NAME and not is_anonymous,
            'display_logout': request.user.is_authenticated and not is_anonymous,
            'display_create_account': request.user.is_authenticated and is_anonymous and allow_account_conversion,
            'display_convert_account_banner': allow_account_conversion and is_anonymous and
            settings.SHOW_CONVERT_ACCOUNT_BANNER,
            'brand_display_name': settings.BRAND_DISPLAY_NAME,
            'copyright_year': settings.COPYRIGHT_YEAR,
            'about_page_path': settings.ABOUT_PAGE_PATH,
            'contact_page_path': settings.CONTACT_PAGE_PATH,
            'is_anonymous': is_anonymous,
        }
    }

from django.conf import settings


def is_site_owner(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and (user.is_staff or user.username == settings.SITE_OWNER_USERNAME)
    )

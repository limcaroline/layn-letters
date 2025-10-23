from django.conf import settings


def site_owner_username(_request):
    return {"SITE_OWNER_USERNAME": settings.SITE_OWNER_USERNAME}

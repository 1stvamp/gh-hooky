from django.conf import settings
from django.contrib.sites.models import Site

def site(context):
    """Provide access to the values such as ENABLE_REGISTRATION
    """
    current_site = Site.objects.get(id=settings.SITE_ID)
    return {'site': current_site}

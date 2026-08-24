from django.conf import settings

from .models import Profile, SocialLink


def site_context(request):
    """Global template context: site metadata + profile/social links used
    on every page (nav, footer)."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "profile": Profile.objects.first(),
        "social_links": SocialLink.objects.all(),
    }

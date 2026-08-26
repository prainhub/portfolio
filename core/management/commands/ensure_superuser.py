import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create an admin login from DJANGO_SUPERUSER_* env vars.

    Exists because hosts without interactive shell access (e.g. Render's
    free web service plan) have no way to run `createsuperuser`
    interactively. Safe to run on every deploy: idempotent, and never
    touches the password of an account that already exists — so changing
    your password in /admin/ later won't get silently reset on the next
    deploy. No-ops entirely if the env vars aren't set.
    """

    help = "Create (or ensure staff/superuser flags on) an admin login from DJANGO_SUPERUSER_* env vars."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not set — skipping."
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
            return

        changed = False
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True
        if changed:
            user.save()
        self.stdout.write(
            f"Superuser '{username}' already exists — left password unchanged."
        )

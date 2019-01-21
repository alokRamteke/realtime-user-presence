from django.conf import settings
from django.db import models
from django.utils import timezone


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
	last_activity = models.DateTimeField(default=timezone.now)

from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from project.models import LoggedInUser, Profile
from django.db.models.signals import post_save


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
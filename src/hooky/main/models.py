from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    github_key = models.CharField(max_length=255, null=True, blank=True)
    github_username = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255, null=True, blank=True)

def user_save_handler(sender, **kwargs):
    # Make sure we create a matching UserProfile instance whenever
    # a new User is created.
    if kwargs['created']:
        up = UserProfile()
        up.user = kwargs['instance']
        up.save()
post_save.connect(user_save_handler, User)

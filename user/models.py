from django.db import models
from django.contrib.auth.models import AbstractUser


# https://www.reddit.com/r/django/comments/2dks92/which_fields_are_unnecessary_to_override_in/
class UserProfile(AbstractUser):
    prompt_list = models.TextField(default='[]')
    story_list = models.TextField(default='[]')

    def __unicode__(self):
        return self.username
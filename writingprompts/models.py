from django.db import models
from user.models import UserProfile


class Prompt(models.Model):
    title = models.CharField(max_length=50)

    content = models.TextField()
    author = models.ForeignKey(UserProfile)
    child_list = models.TextField(default='[]')

    def __unicode__(self):
        return self.title + ' - ' + self.content


class Story(models.Model):
    prompt = models.ForeignKey(Prompt, default=1)

    content = models.TextField()
    author = models.ForeignKey(UserProfile)
    parent_id = models.BigIntegerField(null=True, blank=True)
    child_list = models.TextField(default='[]')

    def __unicode__(self):
        return self.prompt + ' + ' + self.content

from django.db import models
from user.models import UserProfile


class Prompt(models.Model):
    title = models.CharField(max_length=50)

    content = models.TextField()
    author = models.ForeignKey(UserProfile)
    child_list = models.TextField(default='[]')

    def __str__(self):
        return "Prompt " + str(self.pk) + "| child_list: " + self.child_list


class Story(models.Model):
    prompt = models.BigIntegerField(null= True, blank=True)

    content = models.TextField()
    author = models.ForeignKey(UserProfile)
    parent_id = models.BigIntegerField(null=True, blank=True)
    child_list = models.TextField(default='[]')

    def __str__(self):
        return "Story " + str(self.pk) + "| child_list: " + self.child_list + "parent_Id: " + str(self.parent_id)

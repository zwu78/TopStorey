from django.db import models

class Prompt(models.Model):
    title = models.CharField(max_length=50)

    content = models.TextField()
    author = models.CharField(max_length=30, blank=True)  # TODO: To be foreign key of user
    child_list = models.TextField(default='[]')

class Story(models.Model):
    prompt = models.ForeignKey(Prompt, default=1)

    content = models.TextField()
    author = models.CharField(max_length=30) # TODO: To be foreign key of user
    parent_list = models.TextField(default='[]')


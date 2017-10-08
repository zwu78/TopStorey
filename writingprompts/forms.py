from django import forms
from .models import Prompt, Story


class NewPromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ('title', 'content',)

class NewStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = {'content',}
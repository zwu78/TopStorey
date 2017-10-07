from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Prompt

# /writingprompts
def prompt_list(request):
    prompt_list = get_object_or_404(Prompt, id=1)
    request.session.prompt_list = prompt_list
    return render(request, 'prompt_list.html')


# /writingprompts/1
def prompt(request, prompt_id):
    return render(request, 'prompt.html')


# /writingprompts/new
def new_prompt(request):
    return HttpResponse("Hello World")


# /writingprompts/1/story/1
def story(request, prompt_id, story_id):
    return HttpResponse("Hello World")


# /writingprompts/1/story/new
def new_story(request, prompt_id):
    return HttpResponse("Hello World")

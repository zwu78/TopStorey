from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Prompt, Story
from .forms import NewPromptForm, NewStoryForm

import json
# /writingprompts
def prompt_list(request):
    prompt_list = get_object_or_404(Prompt, id=1)

    return render(request, 'prompt_list.html')


# /writingprompts/1
def prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    request.session.is_story = False
    story_list = []

    for story_id in json.loads(prompt.child_list):
        story_list.append(get_object_or_404(Story, pk=story_id))
    return render(request, 'prompt.html', {'prompt': prompt, 'story_list': story_list})


# /writingprompts/new
def new_prompt(request):

    # Form posted
    if request.method == 'POST':
        form = NewPromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.author = request.user
            prompt.save()

        return redirect('writingprompts:prompt', prompt.id)

    # First time visitng
    else:
        form = NewPromptForm()
    return render(request, 'new_prompt.html', {'form': form})


# /writingprompts/1/story/1
def story(request, prompt_id, story_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    story = get_object_or_404(Story, id=story_id)
    request.session['is_story'] = False
    return render(request, 'story.html', {'story': story, 'prompt': prompt})


# /writingprompts/1/story/new
def new_story(request, prompt_id):
    print(request.session.get('is_story'))
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    if request.method == 'POST':
        form = NewStoryForm(request.POST)
        if form.is_valid():

            story = form.save(commit=False)
            story.author = request.user
            story.save()

            if not request.session.is_story:
                story_list = json.loads(prompt.child_list)
                story_list.append(story.id)
                prompt.child_list = json.dumps(story_list)
                prompt.save()

        return redirect('writingprompts:story', prompt_id, story.id)

    # First time visitng
    else:
        form = NewStoryForm()
    return render(request, 'new_story.html', {'form': form})

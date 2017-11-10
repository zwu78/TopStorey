from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Prompt, Story
from user.models import UserProfile
from .forms import NewPromptForm, NewStoryForm

import json


# /writingprompts
def prompt_list(request):
    prompt_list = list(Prompt.objects.all())
    if not prompt_list:
        prompt_list = None

    return render(request, 'prompt_list.html', {'prompt_list': prompt_list})


# /writingprompts/1
def prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    request.session.is_story = False
    story_list = []
    request.session['is_story'] = False
    for story_id in json.loads(prompt.child_list):
        story_list.append(get_object_or_404(Story, pk=story_id))
    return render(request, 'prompt.html', {'prompt': prompt, 'story_list': story_list})


# /writingprompts/new
def new_prompt(request):
    request.session['is_story'] = False
    # Form posted
    if request.method == 'POST':
        form = NewPromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            print(request.user)
            prompt.author = request.user
            prompt.save()

        return redirect('writingprompts:prompt', prompt.id)

    # First time visiting
    else:
        form = NewPromptForm()
    return render(request, 'new_prompt.html', {'form': form})


# /writingprompts/1/story/1
def story(request, prompt_id, story_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    promptChildList = json.loads(prompt.child_list)
    story = get_object_or_404(Story, id=story_id)

    if int(story_id) not in promptChildList:  # Story has parent stories above itself
        request.session['is_story'] = True
        request.session['current_story'] = story_id
        child_story_list = []
        for each in json.loads(story.child_list):
            print(each)
            child_story_list.append(get_object_or_404(Story, id=each))
        if len(child_story_list) == 0:
            child_story_list = None
        return render(request, 'story.html', {'story': story, 'child_story_list': child_story_list})
    else:  # Story is directly below a parent
        request.session['is_story'] = False
        child_story_list = []
        for each in json.loads(prompt.child_list):
            print(each)
            child_story_list.append(get_object_or_404(Story, id=each))
        if len(child_story_list) == 0:
            child_story_list = None
        return render(request, 'story.html', {'story': story, 'prompt': prompt, 'child_story_list': child_story_list})


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
            if request.session['is_story']:
                story.parent_id = request.session['current_story']  # This is actually story_pk
                parentStory = get_object_or_404(Story, pk=prompt_id)  # This is actually story_pk
                parentStory.child_list = json.dumps(json.loads(parentStory.child_list).append(story.id))
                parentStory.save()

                return redirect('writingprompts:story', prompt_id, story.id)
            if not request.session['is_story']:
                print("Appending " + str(story.id) + " child_list for prompt")
                story.parent_id = prompt_id
                story_list = json.loads(prompt.child_list)
                story_list.append(story.id)
                prompt.child_list = json.dumps(story_list)
                prompt.save()
                story.save()

                return redirect('writingprompts:prompt', prompt_id)

    # First time visitng
    else:
        form = NewStoryForm()
    return render(request, 'new_story.html', {'form': form})

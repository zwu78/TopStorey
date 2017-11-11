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
    print(prompt.child_list)
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
    try:
        story = Story.objects.get(pk=story_id)
    except Prompt.DoesNotExist:
        raise Http404("Story not found for " + story_id)

    request.session['is_story'] = True
    request.session['current_story'] = story_id
    child_story_list = []
    for each in json.loads(story.child_list):
        print(each)
        child_story_list.append(get_object_or_404(Story, id=each))
    if len(child_story_list) == 0:
        child_story_list = None
    return render(request, 'story.html', {'prompt_id': prompt_id, 'story': story, 'child_story_list': child_story_list})


# /writingprompts/1/story/new
def new_story(request, prompt_id):
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    if request.method == 'POST':
        form = NewStoryForm(request.POST)
        if form.is_valid():

            new_story = form.save(commit=False)
            new_story.author = request.user
            new_story.save()
            if request.session['is_story']:

                new_story.prompt = prompt.pk
                new_story.parent_id = request.session['current_story']  # This is actually story_pk
                new_story.save()
                parentStory = get_object_or_404(Story, pk=request.session['current_story'])  # This is actually story_pk
                child_list = json.loads(parentStory.child_list)
                child_list.append(new_story.id)
                parentStory.child_list = json.dumps(child_list)

                parentStory.save()

                return redirect('writingprompts:story', prompt_id, parentStory.id)
            else: # if not request.session['is_story']:

                # Gets and add new story id to child_list
                story_list = json.loads(prompt.child_list)
                story_list.append(new_story.id)
                prompt.child_list = json.dumps(story_list)
                prompt.save()
                new_story.save()

                return redirect('writingprompts:prompt', prompt_id)

    # First time visiting
    else:
        form = NewStoryForm()
    return render(request, 'new_story.html', {'form': form})

# /writingprompts/1/story/1/new
def new_story_with_storyId(request, prompt_id, story_id):
    prompt = get_object_or_404(Prompt, pk=prompt_id)
    if request.method == 'POST':
        form = NewStoryForm(request.POST)
        if form.is_valid():

            new_story = form.save(commit=False)
            new_story.author = request.user
            new_story.save()
            if request.session['is_story']:

                new_story.prompt = prompt.pk
                new_story.parent_id = story_id  # This is actually story_pk
                new_story.save()
                parentStory = get_object_or_404(Story, pk=story_id)  # This is actually story_pk
                child_list = json.loads(parentStory.child_list)
                child_list.append(new_story.id)
                parentStory.child_list = json.dumps(child_list)

                parentStory.save()

                return redirect('writingprompts:story', prompt_id, parentStory.id)
            else: # if not request.session['is_story']:

                # Gets and add new story id to child_list
                story_list = json.loads(prompt.child_list)
                story_list.append(new_story.id)
                prompt.child_list = json.dumps(story_list)
                prompt.save()
                new_story.save()

                return redirect('writingprompts:prompt', prompt_id)

    # First time visiting
    else:
        form = NewStoryForm()
    return render(request, 'new_story.html', {'form': form})

from django.conf.urls import url
from . import views

app_name = 'writingprompts'

urlpatterns = [

    # /writingprompts
    url(r'^$', views.prompt_list, name='prompt_list'),

    # /writingprompts/1
    url(r'^(?P<prompt_id>[0-9]+)/$', views.prompt, name='prompt'),

    # /writingprompts/new
    url(r'^new/$', views.new_prompt, name='new_prompt'),

    # /writingprompts/1/story/1
    url(r'^(?P<prompt_id>[0-9]+)/story/(?P<story_id>[0-9]+)/$', views.story, name='story'),

    # /writingprompts/1/story/new
    url(r'^(?P<prompt_id>[0-9]+)/story/new/$', views.new_story, name='new_story'),
]
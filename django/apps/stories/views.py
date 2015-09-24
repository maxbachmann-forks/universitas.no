# -*- coding: utf-8 -*-i
"""
Views for articles
"""
import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from apps.core.views import search_404_view
from .models import Story

logger = logging.getLogger('universitas')


def article_view(request, story_id, **section_and_slug):
    template = 'story.html'
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        slug = section_and_slug.get('slug')
        return search_404_view(request, slug)

    if story.publication_status != Story.STATUS_PUBLISHED:
        raise Http404('You are not supposed to visit this page')

    correct_url = story.get_absolute_url()

    if request.path != correct_url:
        return HttpResponseRedirect(correct_url)

    context = {'story': story, }
    story.visit_page(request)
    return render(request, template, context,)

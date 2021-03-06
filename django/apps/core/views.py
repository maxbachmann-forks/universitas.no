"""Core views for webpage."""

import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from api.adverts import AdvertViewSet
from api.frontpage import FrontpageStoryViewset
from api.issues import IssueViewSet
from api.publicstories import PublicStoryViewSet
from api.site import SiteDataAPIView
from api.user import AvatarUserDetailsSerializer
from apps.frontpage.models import FrontpageStory
from apps.issues.models import Issue
from apps.stories.models import Story
from utils.decorators import cache_memoize

from . import express

logger = logging.getLogger(__name__)


def only_anon(request, *args):
    user_id = 0 if request.user.is_anonymous else request.user.pk
    return [user_id, *args]


@cache_memoize(timeout=60 * 60, args_rewrite=only_anon)
def fetch_user(request):
    if request.user.is_authenticated:
        serializer = AvatarUserDetailsSerializer(
            request.user, context={'request': request}
        )
        payload = json.loads(json.dumps(serializer.data))
        return {'type': 'auth/REQUEST_USER_SUCCESS', 'payload': payload}
    else:
        return {'type': 'auth/REQUEST_USER_FAILED'}


def fetch_story(request, pk):
    response = PublicStoryViewSet.as_view({'get': 'retrieve'})(request, pk=pk)
    payload = {
        **response.data,
        'HTTPstatus': response.status_code,
        'id': pk,
    }
    payload = json.loads(json.dumps(payload))
    return {'type': 'publicstory/STORY_FETCHED', 'payload': payload}


@cache_memoize(timeout=60 * 30, args_rewrite=only_anon)
def fetch_newsfeed(request):
    response = FrontpageStoryViewset.as_view({'get': 'list'})(request)
    payload = json.loads(json.dumps(response.data))
    return {'type': 'newsfeed/FEED_FETCHED', 'payload': payload}


@receiver(post_save, sender=FrontpageStory)
def clear_feed_cache(sender, instance, **kwargs):
    fetch_newsfeed.invalidate_all()


@cache_memoize(timeout=60 * 30, args_rewrite=only_anon)
def fetch_issues(request):
    response = IssueViewSet.as_view({'get': 'list'})(request)
    payload = json.loads(json.dumps({'issues': response.data.get('results')}))
    return {'type': 'issues/ISSUES_FETCHED', 'payload': payload}


@receiver(post_save, sender=Issue)
def clear_issues_cache(sender, instance, **kwargs):
    fetch_issues.invalidate_all()


@cache_memoize(timeout=60 * 15, args_rewrite=only_anon)
def fetch_site(request):
    response = SiteDataAPIView.as_view()(request)
    payload = json.loads(json.dumps(response.data))
    return {'type': 'site/SITE_FETCHED', 'payload': payload}


def fetch_adverts(request):
    response = AdvertViewSet.as_view({'get': 'qmedia'})(request)
    payload = json.loads(json.dumps(response.data))
    return {'type': 'adverts/ADVERTS_FETCH_SUCCESS', 'payload': payload}


def get_redux_actions(request, story=None, issues=None):
    """Redux actions to simulate data prefetching server side rendering."""
    actions = [
        fetch_newsfeed(request),
        fetch_site(request),
        fetch_user(request),
        fetch_adverts(request),
    ]
    if issues:
        actions.append(fetch_issues(request))
    if story:
        actions.append(fetch_story(request, int(story)))
    return actions


@receiver(post_save, sender=Story)
def clear_cached_story_response(sender, instance, **kwargs):
    cache.delete(f'cached_page_{instance.pk}')


def react_frontpage_view(request, section=None, story=None, slug=None):
    """Main view for server side rendered content"""

    is_IE = 'Trident' in request.META.get('HTTP_USER_AGENT', '')
    cache_key = f'cached_page_{story or request.path}{"IE" if is_IE else ""}'

    if request.user.is_anonymous and not settings.DEBUG:
        if story:
            Story.register_visit_in_cache(story)
        response, path = cache.get(cache_key, (None, None))
        if response:
            if path != request.path:
                return redirect(path)
            logger.debug(f'{cache_key} {request}')
            return response

    issues = any(request.path.startswith(word) for word in ('/utg', '/pdf'))
    redux_actions = get_redux_actions(request, story, issues)
    ssr_context = express.react_server_side_render(
        actions=redux_actions,
        url=request.build_absolute_uri(),
        path=request.path,
    )
    if ssr_context.get('error'):
        logger.debug(json.dumps(ssr_context, indent=2))

    try:
        pathname = ssr_context['state']['location']['pathname']
        if pathname != request.path:
            return redirect(pathname)
    except KeyError:
        pass

    status_code = ssr_context.pop('HTTPStatus', 200)
    if status_code == 404 and request.path[-1] != '/':
        return redirect(request.path + '/')

    response = render(
        request,
        template_name='universitas-server-side-render.html',
        context={'ssr': ssr_context, 'IE': is_IE},
        status=status_code,
    )

    if request.user.is_anonymous and status_code == 200:
        timeout = 120
        if request.path != '/':
            timeout *= 60
        cache.set(cache_key, (response, request.path), timeout)

    return response


class TextTemplateView(TemplateView):
    """ Render plain text file. """

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/plain'
        return super().render_to_response(context, **response_kwargs)


class HumansTxtView(TextTemplateView):
    """ humans.txt contains information about who made the site. """

    template_name = 'humans.txt'


class RobotsTxtView(TextTemplateView):
    """ robots.txt contains instructions for webcrawler bots. """

    if settings.DEBUG:
        template_name = 'robots-staging.txt'
    else:
        template_name = 'robots-production.txt'

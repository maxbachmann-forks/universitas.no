from collections import OrderedDict

from rest_framework import pagination, serializers, viewsets
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param

from apps.frontpage.models import FrontpageStory
from apps.photo.models import ImageFile
from apps.stories.models import Story
from django.db.models import Case, Q, When
from utils.serializers import AbsoluteURLField, CropBoxField


def size_validator(value):
    columns, rows = value
    if columns not in [2, 3, 4, 6]:
        raise serializers.ValidationError('Incorrect column size')
    if rows not in [1, 2, 3, 4, 5, 6]:
        raise serializers.ValidationError('Incorrect row size')


class NestedStorySerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='story_type.section')

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'language',
            'section',
        ]


class FrontpageStorySerializer(serializers.ModelSerializer):
    """ModelSerializer for FrontpageStory"""

    image = AbsoluteURLField(source='imagefile.large.url')
    imagefile = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=ImageFile.objects.all(),
        allow_null=True,
    )
    crop_box = CropBoxField(read_only=True, source='imagefile.crop_box')
    section = serializers.IntegerField(
        read_only=True, source='story.story_type.section.pk'
    )
    story = NestedStorySerializer(read_only=True)
    language = serializers.SerializerMethodField()
    ranking = serializers.SerializerMethodField()
    baserank = serializers.SerializerMethodField()
    size = serializers.ListField(
        read_only=False,
        min_length=2,
        max_length=2,
        child=serializers.IntegerField(min_value=1, max_value=10),
        validators=[size_validator],
    )

    def get_ranking(self, instance):
        return instance.ranking

    def get_baserank(self, instance):
        return instance.baserank

    def get_language(self, instance):
        if instance.story.language == 'en':
            return 'eng'
        else:
            return 'nor'

    class Meta:
        model = FrontpageStory
        fields = [
            'id',
            'url',
            'headline',
            'kicker',
            'vignette',
            'lede',
            'html_class',
            'size',
            'published',
            'image',
            'imagefile',
            'crop_box',
            'section',
            'language',
            'story',
            'priority',
            'ranking',
            'baserank',
        ]


class FrontpagePaginator(pagination.LimitOffsetPagination):
    default_limit = 25

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([('count', self.count),
                         ('next', self.get_next_link(data)),
                         ('results', data)])
        )

    def get_next_link(self, data=[]):
        if len(data) < self.limit:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = data[-1]['ranking']
        return replace_query_param(url, self.offset_query_param, offset)

    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request

        if self.offset:
            queryset = queryset.filter(ranking__lt=self.offset)
        return list(queryset[:self.limit])


class FrontpageStoryViewset(viewsets.ModelViewSet):
    """ Frontpage news feed. """

    queryset = FrontpageStory.objects.published().with_ranking(
    ).prefetch_related('imagefile', 'story', 'story__story_type__section')
    serializer_class = FrontpageStorySerializer
    pagination_class = FrontpagePaginator

    def _sections(self, qs):
        section = self.request.query_params.get('section')
        if section:
            try:
                sections = map(int, section.split(','))
                qs = qs.filter(story__story_type__section__in=sections)
            except ValueError:
                pass
        return qs

    def _language(self, qs):
        language = self.request.query_params.get('language')
        english = Q(story__language='en')
        if language == 'eng':
            qs = qs.filter(english)
        if language == 'nor':
            qs = qs.exclude(english)
        return qs

    def _search(self, qs):
        search = self.request.query_params.get('search')
        if search:
            stories = Story.objects.published().search(search)
            pks = stories.values_list('frontpagestory', flat=True)
            if pks:
                order = Case(
                    *[When(pk=pk, then=pos) for pos, pk in enumerate(pks)]
                )
                qs = qs.filter(pk__in=pks).order_by(order)
            else:
                qs = qs.none()
        return qs

    def get_queryset(self):
        """Sort by section"""
        return self._search(
            self._language(self._sections(super().get_queryset()))
        )

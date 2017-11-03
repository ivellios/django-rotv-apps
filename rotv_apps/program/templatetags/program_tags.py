# -*- coding: utf-8 -*-
from django import template
from tagging.models import TaggedItem

from ..models import Episode, Program

register = template.Library()


@register.inclusion_tag('program/_episodes_cards.html')
def similar_episodes_by_tags(episode, limit = 2, size = None, header = None, starting = 0):
    episodes = TaggedItem.objects.get_union_by_model(Episode.objects.active(),
                                                     tags = episode.tags).exclude(pk = episode.pk)
    episodes = episodes.order_by('?')[starting:starting+limit]
    return {'episodes': episodes, 'size': size, 'header': header}


@register.inclusion_tag('program/_episodes_list.html')
def similar_episodes_by_tags_list(tags, limit = 2, size = None, exclude = None, header = None, starting = 0):
    episodes = TaggedItem.objects.get_union_by_model(Episode.objects.active(), tags = tags)
    if exclude:
        episodes = episodes.exclude(pk = exclude.pk)
    return {'episodes': episodes.order_by('?')[starting:starting+limit], 'size': size, 'header': header}


@register.inclusion_tag('program/_episodes_list.html')
def recent_episodes(limit = 6, exclude = None, header = None, starting = 0):
    episodes = Episode.published.all()
    if exclude:
        episodes = episodes.exclude(pk = exclude.pk)
    return {'episodes': episodes.order_by('-publish_time')[starting:starting+limit], 'header': header}


@register.inclusion_tag('program/_episodes_list.html')
def promoted_episodes(limit = 6, exclude = None, header = None, starting = 0):
    episodes = Episode.published.filter(promoted = True)
    if exclude:
        episodes = episodes.exclude(pk = exclude.pk)
    return {'episodes': episodes.order_by('-publish_time')[starting:starting+limit], 'header': header}


@register.inclusion_tag('program/_episodes_cards.html')
def promoted_episodes_cards(limit = 6, exclude = None, header = None, starting = 0, columns = None):
    episodes = Episode.published.filter(promoted = True)
    if exclude:
        episodes = episodes.exclude(pk = exclude.pk)
    return {'episodes': episodes.order_by('-publish_time')[starting:starting+limit], 'header': header, 'columns': columns}


@register.inclusion_tag('program/similar_programs.html')
def similar_programs_by_tags(episode, header = None):
    programs = TaggedItem.objects.get_union_by_model(Program, tags = episode.tags).order_by('?')[:2]
    return {'programs': programs, 'header': header}

# -*- coding: utf-8 -*-

from django import template
from tagging.models import TaggedItem

from ..models import Entry

register = template.Library()


@register.inclusion_tag('blog/_entries_collection.html')
def similar_entries_by_tags(tags, limit=8, exclude=None, header=None):
    entries = TaggedItem.objects.get_union_by_model(Entry, tags=tags)
    if exclude:
        entries = entries.exclude(pk=exclude.pk)
    return {'entries': entries[:limit], 'header': header}


@register.inclusion_tag('blog/_entries_collection.html')
def blog_last_entries(limit=3, current=None, header=None):
    entries = Entry.published.all()[:limit]
    return {'entries': entries, 'current': current, 'header': header}

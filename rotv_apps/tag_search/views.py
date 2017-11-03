# -*- coding: utf-8 -*-
import re
import operator

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.utils.http import urlquote_plus, urlunquote_plus
from django.views.generic import ListView, TemplateView
from django.views.generic.base import RedirectView

from tagging.models import TaggedItem, Tag

from ..program.models import Episode
from ..blog.models import Entry


class TagQueryHelper(object):
    def __init__(self, tags_query, **kwargs):
        self.uquery = urlunquote_plus(tags_query)

    def get_tagged_items(self, cls, ):
        tag_query = self.get_tag_list()
        quoted = re.findall(r'\"(.+?)\"', ', '.join(tag_query))
        if quoted:
            tag_query = [tag.replace('"','') for tag in tag_query]
            query = reduce(operator.or_, [Q(name = element) for element in tag_query])
        else:
            query = reduce(operator.or_, [Q(name__contains = element) for element in tag_query])
        tags = Tag.objects.filter(query)
        return TaggedItem.objects.get_union_by_model(cls, tags)

    def get_tag_list(self):
        tags = [tag.strip() for tag in self.uquery.split('+')]
        return tags


class ObjectsByTagView(ListView):
    paginate_by = 8
    tqp = None

    def __init__(self, **kwargs):
        super(ObjectsByTagView, self).__init__()

    def get_queryset(self, ):
        self.tqp = TagQueryHelper(self.kwargs.get('tags', ''))
        return self.tqp.get_tagged_items(self.cls)

    def get_context_data(self, **kwargs):
        context = super(ObjectsByTagView, self).get_context_data(**kwargs)
        context['tag_query'] = self.tqp.get_tag_list()
        context['tag_query_raw'] = self.kwargs.get('tags', '')
        return context


class SearchObjectsByTagsView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        s = self.request.GET.get('search', None)
        if not s:
            s = self.request.POST.get('search', None)
        if not s:
            raise Http404
        surl = urlquote_plus(s.replace(' ', '+'))
        return reverse(self.redirect_url_name, kwargs = {'tags': surl})


class SearchByTagsView(SearchObjectsByTagsView):
    redirect_url_name = 'tag_search_results'


class SearchResultsView(TemplateView):
    template_name = 'tag_search/results.html'
    
    def get_context_data(self, **kwargs):
        tqp = TagQueryHelper(self.kwargs.get('tags', ''))
        entries = tqp.get_tagged_items(Entry)
        episodes = tqp.get_tagged_items(Episode)
        # now put it into the context
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['entries'] = entries[:5]
        context['episodes'] = episodes[:5]
        context['all_entries'] = entries
        context['all_episodes'] = episodes
        context['tag_query'] = tqp.get_tag_list()
        context['tag_query_raw'] = self.kwargs.get('tags', '')
        return context

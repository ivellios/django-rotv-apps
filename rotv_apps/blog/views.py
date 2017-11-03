# -*- coding: utf-8 -*-
# Create your views here.

from django.views.generic import DetailView, ListView
from ..tag_search.views import ObjectsByTagView, SearchObjectsByTagsView

from .models import Entry


class EntryView(DetailView):
    model = Entry

    def get_queryset(self):
        return Entry.published.filter(slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(EntryView, self).get_context_data(**kwargs)
        context['detailed'] = True
        return context


class ArchiveView(ListView):
    model = Entry
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context


class EntriesByTagView(ObjectsByTagView):
    """
        Shows the list of entries with a given tag.
        Can show for mutiple tags, but due to
        the URL logic it should not be used for that.
    """
    template_name = 'blog/entry_tagged_list.html'
    cls = Entry


class EntriesBySearchedTagsView(ObjectsByTagView):
    """
        This is almost the same as EntriesByTag,
        except it shows results for multiple tags' search.
    """
    template_name = 'blog/entry_tagged_search_list.html'
    cls = Entry


class SearchEntriesByTagsView(SearchObjectsByTagsView):
    """
        Grabs the search arguments from the forms
        and redirects to the
    """
    redirect_url_name = 'blog_search_by_tags'

from django.conf.urls import  url

from .program.views import (EpisodeView,
                            ProgramListView, IndexView, EpisodesByTagView,
                            SearchEpisodeByTagsView, EpisodesBySearchedTagsView,
                            ProgramDetailView)
from .blog.views import (EntryView, ArchiveView, EntriesByTagView, SearchEntriesByTagsView,
                         EntriesBySearchedTagsView)
from .tag_search.views import SearchByTagsView, SearchResultsView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^serie/$', ProgramListView.as_view(), name='program_list'),
    url(r'^program/(?P<slug>[\w_-]+)/?$', ProgramDetailView.as_view(), name='program_detail'),
    url(r'^ogladaj/(?P<program_slug>[\w_-]+)/(?P<number>\d+)/?$', EpisodeView.as_view(), name='program_episode_detail'),
    url(r'^odcinki/tag/(?P<tags>[\w\%\&\+\._-]+)/?$', EpisodesByTagView.as_view(), name='program_episode_tag'),
    url(r'^odcinki/szukaj/?$', SearchEpisodeByTagsView.as_view(), name='program_episode_search'),
    url(r'^odcinki/szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', EpisodesBySearchedTagsView.as_view(),
        name='program_episode_search_by_tags'),

    url(r'^blog/tag/(?P<tags>[\w\%\&\+\._-]+)/?$', EntriesByTagView.as_view(), name='blog_tag'),
    url(r'^blog/szukaj/?$', SearchEntriesByTagsView.as_view(), name='blog_search'),
    url(r'^blog/szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', EntriesBySearchedTagsView.as_view(), name='blog_search_by_tags'),
    url(r'^blog/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w_-]+)/?$', EntryView.as_view(), name='blog_entry'),
    url(r'^blog/?$', ArchiveView.as_view(), name='blog_archive'),

    url(r'^szukaj/?$', SearchByTagsView.as_view(), name='tag_search_search'),
    url(r'^szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', SearchResultsView.as_view(), name='tag_search_results'),
]
from django.conf.urls import url, include

from .program.views import (EpisodeProgramView, EpisodePlaylistView,
                            ProgramListView, IndexView, EpisodesByTagView,
                            SearchEpisodeByTagsView, EpisodesBySearchedTagsView,
                            ProgramDetailView)
from .blog.views import (EntryView, ArchiveView, EntriesByTagView, SearchEntriesByTagsView,
                         EntriesBySearchedTagsView)
from .tag_search.views import SearchByTagsView, SearchResultsView
from .partners.views import MediaPatronageRequestConfirmView, MediaPatronageRequestView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^serie/$', ProgramListView.as_view(), name='program_list'),
    url(r'^program/(?P<slug>[\w_-]+)/?$', ProgramDetailView.as_view(), name='program_detail'),
    url(r'^watch/program/(?P<program_slug>[\w_-]+)/(?P<episode_slug>[\w_-]+)/?$',
        EpisodeProgramView.as_view(), name='program_episode_detail'),
    url(r'^watch/playlist/(?P<playlist_slug>[\w_-]+)/(?P<episode_slug>[\w_-]+)/?$',
        EpisodePlaylistView.as_view(), name='playlist_episode_detail'),
    url(r'^odcinki/tag/(?P<tags>[\w\%\&\+\._-]+)/?$', EpisodesByTagView.as_view(), name='program_episode_tag'),
    url(r'^odcinki/szukaj/?$', SearchEpisodeByTagsView.as_view(), name='program_episode_search'),
    url(r'^odcinki/szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', EpisodesBySearchedTagsView.as_view(),
        name='program_episode_search_by_tags'),

    url(r'^events/partners/add/confirm/?$', MediaPatronageRequestConfirmView.as_view(), name='event_request_confirm'),
    url(r'^events/partners/add/?$', MediaPatronageRequestView.as_view(), name='event_request'),


    url(r'^blog/tag/(?P<tags>[\w\%\&\+\._-]+)/?$', EntriesByTagView.as_view(), name='blog_tag'),
    url(r'^blog/szukaj/?$', SearchEntriesByTagsView.as_view(), name='blog_search'),
    url(r'^blog/szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', EntriesBySearchedTagsView.as_view(), name='blog_search_by_tags'),
    url(r'^blog/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w_-]+)/?$', EntryView.as_view(), name='blog_entry'),
    url(r'^blog/?$', ArchiveView.as_view(), name='blog_archive'),

    url(r'^szukaj/?$', SearchByTagsView.as_view(), name='tag_search_search'),
    url(r'^szukaj/(?P<tags>[\w\%\&\+\._-]+)/?$', SearchResultsView.as_view(), name='tag_search_results'),

    url(r'^tinymce/', include('tinymce.urls')),
]

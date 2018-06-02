# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..tag_search.views import ObjectsByTagView, SearchObjectsByTagsView
from ..partners.models import Partner, MediaPatron, MediaPatronage, Colaborator, NormalMediaPatronage
from ..blog.models import Entry
from ..heros.models import HeroEntry

from .models import Episode, Program, Playlist


class EpisodeView(generic.TemplateView):
    template_name = 'program/episode_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EpisodeView, self).get_context_data(**kwargs)
        context['episode'] = get_object_or_404(Episode,
                                               slug=kwargs.get('episode_slug'))
        return context


class EpisodeProgramView(generic.TemplateView):
    template_name = 'program/program_episode_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EpisodeProgramView, self).get_context_data(**kwargs)
        context['episode'] = get_object_or_404(Episode,
                                               program__slug=kwargs.get('program_slug'),
                                               slug=kwargs.get('episode_slug'))
        return context


class EpisodePlaylistView(generic.TemplateView):
    template_name = 'program/playlist_episode_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EpisodePlaylistView, self).get_context_data(**kwargs)
        context['episode'] = get_object_or_404(Episode,
                                               playlist__slug=kwargs.get('playlist_slug'),
                                               slug=kwargs.get('episode_slug'))
        context['playlist'] = get_object_or_404(Playlist,
                                                slug=kwargs.get('playlist_slug'),)
        return context


class ProgramDetailView(generic.DetailView):
    model = Program


class ProgramListView(generic.ListView):
    template_name = 'program/program_list.html'
    model = Program


class IndexView(generic.TemplateView):
    template_name = 'program/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['recent_blog_posts'] = Entry.published.all()[:3]
        context['hero_list'] = HeroEntry.published.all()[:5]
        context['recent_episodes'] = Episode.published.all().order_by('-added')[:5]
        context['promoted'] = Episode.published.filter(promoted=True).order_by('-added')[:6]
        context['partners'] = Partner.objects.filter(active=True).order_by('name')
        context['patrons'] = MediaPatron.objects.filter(active=True).order_by('name')
        context['colaborators'] = Colaborator.objects.filter(active=True).order_by('name')
        context['upcoming_patronage_list'] = MediaPatronage.upcoming.all()
        context['media_patronage_list'] = MediaPatronage.future.exclude(id__in = context['upcoming_patronage_list'])
        normal_patronage = NormalMediaPatronage.objects.filter(active=True,
                                                               end__gte = timezone.now().date())
        context['normalpatronage'] = normal_patronage.order_by('end')
        return context


class EpisodesByTagView(ObjectsByTagView):
    """
        Shows the episodes with a given tag.
        Can show more than one tag, but should not be used that way.
    """
    template_name = 'program/episode_tagged_list.html'
    cls = Episode


class EpisodesBySearchedTagsView(ObjectsByTagView):
    """
        Shows the episodes by searched tags. Mutiple this time.
    """
    template_name = 'program/episode_tagged_search_list.html'
    cls = Episode


class SearchEpisodeByTagsView(SearchObjectsByTagsView):
    redirect_url_name = 'program_episode_search_by_tags'

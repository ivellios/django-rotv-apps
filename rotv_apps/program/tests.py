from __future__ import print_function
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone
import faker

from .factories import ProgramFactory, EpisodeFactory, HostFactory
from .models import Program, Episode, Host, Playlist
from .utils import get_slug

faker = faker.Factory.create()


class EpisodeQuerySetTest(TestCase):
    def setUp(self):
        self.e1 = EpisodeFactory(publish_time=faker.past_date())
        self.e2 = EpisodeFactory(publish_time=faker.future_date())

    def test_active_queryset(self):
        q = Episode.objects.active()

        self.assertEqual(q.count(), 2)

    def test_before(self):
        """
            Returns object that start on the given date or before it
        """
        q = Episode.objects.before(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.e1, q)

    def test_after(self):
        """
            Return objects that end on the given date or after it.
        """
        q = Episode.objects.after(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.e2, q)

    def test_get_next_to(self):
        # given
        program = ProgramFactory()
        e1 = EpisodeFactory(publish_time='2018-01-02', program=program)
        e2 = EpisodeFactory(publish_time='2018-01-01', program=program)
        qs = Episode.published.filter(program=program)

        # when
        next = qs.get_next_to(e1)

        # then
        self.assertEqual(next.id, e2.id)

    def test_get_prev_to(self):
        # given
        program = ProgramFactory()
        e1 = EpisodeFactory(publish_time='2018-01-02', program=program)
        e2 = EpisodeFactory(publish_time='2018-01-01', program=program)
        qs = Episode.published.filter(program=program)

        # when
        prev = qs.get_next_to(e2)

        # then
        self.assertEqual(prev.id, e1.id)


class PublishedEpisodeManagerTest(TestCase):
    def test_queryset_returns_currently_active_episodes(self):
        e1 = EpisodeFactory(publish_time=faker.past_date())
        e2 = EpisodeFactory(publish_time=faker.future_date())

        q = Episode.published.all()

        self.assertEqual(q.count(), 1)
        self.assertIn(e1, q)


class EpisodeTest(TestCase):
    def setUp(self):
        self.e1 = EpisodeFactory(publish_time='2018-01-03',)
        self.e2 = EpisodeFactory(publish_time='2018-01-02', program=self.e1.program)
        self.e3 = EpisodeFactory(publish_time='2018-01-01', program=self.e1.program)

    def test_get_next_episode(self):
        e = self.e1.get_next_episode()

        self.assertEqual(e.id, self.e2.id)

    def test_get_previous_episode(self):
        e = self.e2.get_previous_episode()

        self.assertEqual(e.id, self.e1.id)

    def test_get_number(self):
        """
        Method should return program name for formatted number of episode like #00.
        :return:
        """
        num_string = self.e1.get_number()

        self.assertEqual(num_string, "{} #{:01d}".format(self.e1.program, self.e1.number))


class ProgramTest(TestCase):
    def setUp(self):
        self.p1 = ProgramFactory()
        self.p2 = ProgramFactory()
        self.p1_episodes = EpisodeFactory.build_batch(10, program=self.p1, publish_time=faker.past_date())
        [e.save() for e in self.p1_episodes]
        self.p2_episodes = EpisodeFactory.build_batch(10, program=self.p2, publish_time=faker.past_date())
        [e.save() for e in self.p2_episodes]

    def test_get_image(self):
        """
        Should return last episode's image
        """
        e = EpisodeFactory(program=self.p1)
        image = self.p1.get_image()

        self.assertEqual(image, e.image)

    def test_get_aboslute_url(self):
        url = self.p1.get_absolute_url()
        self.assertEqual(url, '/series/{}'.format(self.p1.slug))

    def test_get_episode_list(self):
        """
        Returns all episodes of the program.
        """
        eps = self.p1.get_episode_list()
        self.assertEqual(len(self.p1_episodes), eps.count())

    def test_get_episode_brief(self):
        """
        Returns episode list limited to 6 most recent
        """
        eps = self.p1.get_episode_brief()
        self.assertEqual(eps.count(), 6)

    def test_get_last_episode(self):
        # given
        last = Episode.published.order_by('-number').filter(program=self.p1).first()

        # when
        ep = self.p1.get_last_episode()

        # then
        self.assertEqual(ep, last)


class UtilsTest(TestCase):

    def test_get_slug(self):
        # when
        new_slug = get_slug(Episode, 'slug')

        # then
        self.assertEqual(new_slug, 'slug')

    def test_get_slug_exists(self):
        # given
        EpisodeFactory.create(slug='slug')

        # when
        new_slug = get_slug(Episode, 'slug')

        # then
        self.assertEqual(new_slug, 'slug-1')


class PlaylistManagerTest(TestCase):
    def test_create_from_program(self):
        # given
        program = ProgramFactory()
        e1 = EpisodeFactory(program=program, number=1)
        e2 = EpisodeFactory(program=program, number=2)
        e3 = EpisodeFactory(program=program, number=3)

        # when
        playlist = Playlist.objects.create_from_program(program)

        # then
        self.assertEqual(playlist.episodes.count(), 3)
        self.assertEqual(playlist.playlist_episodes.first().position, e1.number)
        self.assertEqual(playlist.playlist_episodes.all()[1].position, e2.number)
        self.assertEqual(playlist.playlist_episodes.all()[2].position, e3.number)
        self.assertEqual(playlist.name, program.name)
        self.assertEqual(playlist.description, program.desc)

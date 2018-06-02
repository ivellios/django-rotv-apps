from __future__ import print_function
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone
import faker

from .factories import ProgramFactory, EpisodeFactory, HostFactory
from .models import Program, Episode, Host
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


class PublishedEpisodeManagerTest(TestCase):
    def test_queryset_returns_currently_active_episodes(self):
        e1 = EpisodeFactory(publish_time=faker.past_date())
        e2 = EpisodeFactory(publish_time=faker.future_date())

        q = Episode.published.all()

        self.assertEqual(q.count(), 1)
        self.assertIn(e1, q)


class EpisodeTest(TestCase):
    def setUp(self):
        self.e1 = EpisodeFactory()
        self.e2 = EpisodeFactory(number=self.e1.number + 1, program=self.e1.program)
        self.e3 = EpisodeFactory(number=self.e2.number + 1, program=self.e1.program)

    def test_get_next_episode(self):
        e = self.e1.get_next_episode()

        self.assertEqual(e, self.e2)

    def test_get_previous_episode(self):
        e = self.e2.get_previous_episode()

        self.assertEqual(e, self.e1)

    def test_get_next_url(self):
        url = self.e1.get_next_url()

        self.assertEqual(url, self.e2.get_absolute_url())

    def test_get_previous_url(self):
        url = self.e2.get_previous_url()

        self.assertEqual(url, self.e1.get_absolute_url())

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
        self.assertEqual(url, '/program/{}'.format(self.p1.slug))

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
        ep = self.p1.get_last_episode()
        last = Episode.published.order_by('-number').filter(program=self.p1).first()
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
        self.assertEqual(new_slug, 'slug_1')

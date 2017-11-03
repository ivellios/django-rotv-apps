from __future__ import print_function
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone
import faker


from .factories import HeroFactory, HeroEntryFactory
from .models import HeroEntry

faker = faker.Factory.create()


class HeroEntryQuerySetTest(TestCase):
    def setUp(self):
        self.h1 = HeroEntryFactory(publish_time=faker.past_date())
        self.h2 = HeroEntryFactory(publish_time=faker.future_date())

    def test_active_queryset(self):
        q = HeroEntry.objects.active()

        self.assertEqual(q.count(), 2)

    def test_before(self):
        """
            Returns object that start on the given date or before it
        """
        q = HeroEntry.published.before(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.h1, q)

    def test_after(self):
        """
            Return objects that end on the given date or after it.
        """
        q = HeroEntry.objects.after(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.h2, q)

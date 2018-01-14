from __future__ import print_function
from dateutil.relativedelta import relativedelta
from django.test import TestCase
import faker


from .factories import MediaPatronageFactory
from .models import MediaPatronage

faker = faker.Factory.create()


class MediaPatronageQuerySetTest(TestCase):
    def test_active_queryset(self):
        MediaPatronageFactory()
        MediaPatronageFactory(active=False)

        q = MediaPatronage.objects.active()

        self.assertEqual(q.count(), 1)

    def test_before(self):
        """
            Returns object that start on the given date or before it
        """
        e1 = MediaPatronageFactory()
        e2_start = e1.end + relativedelta(days=7)
        e2_end = e2_start + relativedelta(days=3)
        MediaPatronageFactory(start=e2_start, end=e2_end)

        date = e2_start + relativedelta(days=-1)

        q = MediaPatronage.objects.before(date)

        self.assertEqual(q.count(), 1)

    def test_after(self):
        """
            Return objects that end on the given date or after it.
        """
        e1 = MediaPatronageFactory()
        e2_start = e1.end + relativedelta(days=7)
        e2_end = e2_start + relativedelta(days=3)
        e2 = MediaPatronageFactory(start=e2_start, end=e2_end)

        date = e1.end + relativedelta(days=1)

        q = MediaPatronage.objects.after(date)

        self.assertEqual(q.count(), 1)


class MediaPatronageManagersTest(TestCase):
    def test_future_has_only_future_objects(self):
        past_date_start = faker.date_time_between(start_date='-30d', end_date='-4d').date()
        past_date_end = past_date_start + relativedelta(days=3)
        MediaPatronageFactory(start=past_date_start, end=past_date_end)
        MediaPatronageFactory()

        q = MediaPatronage.future.all()

        self.assertEqual(q.count(), 1)

    def test_upcomming_objects_are_all_closest(self):
        """
            upcomming objects should return next event in timeline + all events that start
            during that event - thus all events that are parallel
        """
        event1 = MediaPatronageFactory.create()
        event2_start = event1.end + relativedelta(days=-1)
        event2_end = event2_start + relativedelta(days=3)
        event2 = MediaPatronageFactory(start=event2_start, end=event2_end)

        q = MediaPatronage.upcoming.all()

        self.assertEqual(q.count(), 2)


class MediaPatronageTest(TestCase):
    def test_send_create_notification_mail(self):
        from django.core import mail
        from django.conf import settings
        event1 = MediaPatronageFactory.create()
        event1.send_create_notification_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, settings.PATRONAGE_MANAGERS)

    def test_setting_active_changes_activation_time(self):
        event = MediaPatronageFactory.create(active=False)
        event.active = True
        event.save()

        event.refresh_from_db()

        self.assertIsNotNone(event)

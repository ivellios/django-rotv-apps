from __future__ import print_function
from django.test import TestCase
from django.utils import timezone
import faker

from .templatetags.blog_filters import read_more
from .templatetags.blog_tags import similar_entries_by_tags, blog_last_entries
from .factories import EntryFactory, CategoryFactory
from .models import Entry

faker = faker.Factory.create()


class EntryTest(TestCase):
    def setUp(self):
        category = CategoryFactory.create()
        self.entry = EntryFactory.create(categories=(category,))

    def test_get_absolute_url(self):
        url = "/blog/{}/{}/{}".format(self.entry.posted.year,
                                      self.entry.posted.month,
                                      self.entry.slug)
        gen_url = self.entry.get_absolute_url()

        self.assertEqual(url, gen_url)


class EntryQuerySetTest(TestCase):
    def setUp(self):
        self.e1 = EntryFactory(publish_time=faker.past_date(), active=True)
        self.e2 = EntryFactory(publish_time=faker.future_date(), active=True)

    def test_active_queryset(self):
        q = Entry.objects.active()

        self.assertEqual(q.count(), 2)

    def test_before(self):
        """
            Returns object that start on the given date or before it
        """
        q = Entry.objects.before(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.e1, q)

    def test_after(self):
        """
            Return objects that end on the given date or after it.
        """
        q = Entry.objects.after(timezone.now())

        self.assertEqual(q.count(), 1)
        self.assertIn(self.e2, q)


class PublishedEntryManagerTest(TestCase):
    def test_queryset_returns_currently_active_episodes(self):
        e1 = EntryFactory(publish_time=faker.past_date(), active=True)
        e2 = EntryFactory(publish_time=faker.future_date(), active=True)

        q = Entry.published.all()

        self.assertEqual(q.count(), 1)
        self.assertIn(e1, q)


class SimilarEntriesTagTest(TestCase):
    def setUp(self):
        self.entry1 = EntryFactory(new_tags = 'entry,tag1')
        self.entry2 = EntryFactory(new_tags = 'entry,tag2')

    def test_similar_entries_by_tags_for_similar_entries(self):
        data = similar_entries_by_tags(self.entry1.new_tags)
        self.assertIn(self.entry2, data['entries'])
        self.assertIn(self.entry1, data['entries'])

    def test_similar_entries_by_tags_can_exclude_entry(self):
        data = similar_entries_by_tags(self.entry1.new_tags, exclude=self.entry1)
        self.assertIn(self.entry2, data['entries'])
        self.assertNotIn(self.entry1, data['entries'])

    def test_similar_entries_by_tags_limit_to_8_by_default(self):
        EntryFactory.create_batch(8, new_tags = 'entry,tag1')
        data = similar_entries_by_tags(self.entry1.new_tags)
        self.assertEqual(data['entries'].count(), 8)

    def test_similar_entries_by_tags_can_set_header(self):
        TEST_HEADER = 'HEADER_TEST'
        data = similar_entries_by_tags(self.entry1.new_tags, header=TEST_HEADER)
        self.assertEqual(data['header'], TEST_HEADER)


class BlogLastEntriesTagTest(TestCase):
    def setUp(self):
        EntryFactory.create_batch(10, active=True)

    def test_blog_last_entries_returns_3_entries(self):
        data = blog_last_entries()
        self.assertEqual(data['entries'].count(), 3)

    def test_blog_last_entries_can_set_header(self):
        TEST_HEADER = 'HEADER_TEST'
        data = blog_last_entries(header=TEST_HEADER)
        self.assertEqual(data['header'], TEST_HEADER)


class ReadMoreFilterTest(TestCase):
    def setUp(self):
        self.entry = EntryFactory(text=faker.words(5))

        self.truncation_text = "Czytaj dalej"
        self.url = 'http://example.com'

    def test_read_more(self):
        text = read_more(self.entry.text, self.url)
        self.assertIn(self.truncation_text, text)

    def test_read_more_cuts_where_is_more_tag(self):
        pre_more = faker.paragraphs(3)
        after_more = faker.paragraphs(3)
        more_tag = '<!--more-->'
        entry_more_text = '{}{}{}'.format(pre_more, more_tag, after_more)
        more_entry = EntryFactory(text=entry_more_text)

        text = read_more(more_entry.text, self.url)

        self.assertIn(str(pre_more), text)
        self.assertNotIn(str(after_more), text)
        self.assertNotIn(more_tag, text)

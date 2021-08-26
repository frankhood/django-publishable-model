import datetime

from django.test import TestCase
from django.utils import timezone

from publishable_model.querysets import PublishableQuerySet
from publishable_model.settings import *
from tests.example.models import News


class QuerySetTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.publishable_queryset = PublishableQuerySet(News)

    # =======================================================================
    # ./manage.py test tests.test_querysets.QuerySetTest  --settings=tests.settings
    # =======================================================================

    def test_published_items(self):

        news = News()
        news.publish()

        self.assertIn(news, self.publishable_queryset.published_items())
        self.assertNotIn(news, self.publishable_queryset.not_published_items())
        self.assertNotIn(news, self.publishable_queryset.draft_items())

        news2 = News(status=PUBLICATION_STATUS_DRAFT)
        news2.save()

        self.assertNotIn(news2, self.publishable_queryset.published_items())
        self.assertEqual(len(self.publishable_queryset.published_items()), 1)
        self.assertNotIn(news2, self.publishable_queryset.published_items())

    def test_draft_items(self):
        news = News()
        news.save()

        self.assertEqual(len(self.publishable_queryset.draft_items()), 1)
        self.assertIn(news, self.publishable_queryset.draft_items())
        self.assertIn(news, self.publishable_queryset.not_published_items())
        self.assertNotIn(news, self.publishable_queryset.published_items())

    def test_not_published_items(self):

        news = News(publication_start=timezone.now() + datetime.timedelta(days=1))
        news.save()

        self.assertIn(news, self.publishable_queryset.not_published_items())
        self.assertIn(news, self.publishable_queryset.draft_items())
        self.assertNotIn(news, self.publishable_queryset.published_items())

        news.publish(update_publication_start=True)

        self.assertNotIn(news, self.publishable_queryset.not_published_items())
        self.assertIn(news, self.publishable_queryset.published_items())
        self.assertNotIn(news, self.publishable_queryset.draft_items())

        news.unpublish()

        self.assertIn(news, self.publishable_queryset.draft_items())
        self.assertIn(news, self.publishable_queryset.not_published_items())
        self.assertNotIn(news, self.publishable_queryset.published_items())

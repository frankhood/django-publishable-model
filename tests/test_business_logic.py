from copy import copy

from django.test import TestCase
from django.utils import timezone

from publishable_model.settings import *
from tests.example.models import News


class BusinessLogicTest(TestCase):
    # =======================================================================
    # ./manage.py test tests.test_business_logic.BusinessLogicTest  --settings=tests.settings
    # =======================================================================

    def test_new_news_is_drafted_news(self):
        news = News()
        self.assertEqual(news.status, PUBLICATION_STATUS_DRAFT)
        self.assertIsNone(news.publication_start)
        self.assertIsNone(news.publication_end)

    def test_commit_on_new_published_news(self):
        news = News()
        news.publish(commit=False)
        self.assertEqual(news.status, PUBLICATION_STATUS_PUBLISHED)
        self.assertIsNone(news.publication_start)
        self.assertIsNone(news.publication_end)

        news.unpublish(commit=False)
        self.assertEqual(news.status, PUBLICATION_STATUS_DRAFT)

        news.publish()
        self.assertEqual(news.status, PUBLICATION_STATUS_PUBLISHED)
        self.assertIsNotNone(news.publication_start)
        self.assertEqual(news.publication_start.date(), timezone.now().date())
        self.assertIsNone(news.publication_end)

    def test_ways_to_unpublish_news_change_status(self) -> None:
        news = News()
        news.publish()
        self.assertTrue(news.is_actual)

        news_2 = copy(news)
        self.assertTrue(news_2.is_actual)
        self.assertEqual(news_2.status, PUBLICATION_STATUS_PUBLISHED)
        self.assertEqual(news.publication_start, news_2.publication_start)
        self.assertEqual(news.publication_end, news_2.publication_end)
        self.assertEqual(news.status, news_2.status)

        news.unpublish(commit=False)
        self.assertEqual(news.status, PUBLICATION_STATUS_DRAFT)
        self.assertIsNotNone(news.publication_start)
        self.assertIsNone(news.publication_end)

        self.assertFalse(news.is_actual)
        self.assertTrue(news_2.is_actual)
        self.assertEqual(news_2.status, PUBLICATION_STATUS_PUBLISHED)

        news_2.unpublish(commit=False, update_publication_start=True, update_publication_end=False)
        self.assertEqual(news_2.status, PUBLICATION_STATUS_DRAFT)
        self.assertNotEqual(news.publication_start, news_2.publication_start)
        self.assertEqual(news.publication_end, news_2.publication_end)
        self.assertEqual(news.status, news_2.status)
        self.assertFalse(news_2.is_actual)

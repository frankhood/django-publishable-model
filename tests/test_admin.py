import sys
from unittest.mock import patch

from django.test import TestCase
from django.utils import formats, timezone
from django.utils.timezone import localtime, get_current_timezone

from tests.example.admin import NewsAdmin
from tests.example.models import News


class AdminTest(TestCase):

    # =======================================================================
    # ./manage.py test tests.test_admin.AdminTest  --settings=tests.settings
    # =======================================================================

    import platform
    print(platform.python_version())

    def test_get_list_filter(self):

        admin = NewsAdmin(News, '')

        from publishable_model.admin import IsPublishedFilter
        self.assertEquals(len(admin.get_list_filter(request=None)), 1)
        self.assertIn(IsPublishedFilter, admin.get_list_filter(request=None))

    def test_get_list_display(self):

        admin = NewsAdmin(News, '')

        list_display_output = admin.get_list_display(request=None)

        self.assertEqual(admin.DISPLAY_PUBLICATION_DATES, True)

        self.assertIn('display_actual_status', list_display_output)
        self.assertIn('display_publication_dates', list_display_output)
        self.assertNotIn('display_publication_start', list_display_output)
        self.assertNotIn('display_publication_end', list_display_output)

        with patch.object(NewsAdmin, 'DISPLAY_PUBLICATION_START', True):
            admin = NewsAdmin(News, '')
            new_list_display_output = admin.get_list_display(request=None)
            self.assertIn('display_actual_status', new_list_display_output)
            self.assertIn('display_publication_dates', new_list_display_output)
            self.assertIn('display_publication_start', new_list_display_output)

        with patch.object(NewsAdmin, 'DISPLAY_PUBLICATION_END', True):
            admin = NewsAdmin(News, '')
            new_list_display_output = admin.get_list_display(request=None)
            self.assertIn('display_actual_status', new_list_display_output)
            self.assertIn('display_publication_dates', new_list_display_output)
            self.assertIn('display_publication_end', new_list_display_output)

    def test_display_actual_status(self):

        news = News()
        news.publish()

        news2 = News()
        news2.save()

        admin = NewsAdmin(News, '')

        self.assertEqual(admin.display_actual_status(news), True)
        self.assertEqual(admin.display_actual_status(news2), False)

        news.unpublish()

        self.assertEqual(admin.display_actual_status(news), False)

    def test_display_publication_start(self):

        news = News()
        news.publish()

        admin = NewsAdmin(News, '')

        publication_start_value = formats.date_format(localtime(news.publication_start, get_current_timezone()),
                                   "SHORT_DATETIME_FORMAT")

        self.assertEqual(admin.display_publication_start(news), publication_start_value)

    def test_display_publication_end(self):

        news = News(publication_end=timezone.now())
        news.publish()

        admin = NewsAdmin(News, '')

        publication_end_value = formats.date_format(localtime(news.publication_end, get_current_timezone()),
                                   "SHORT_DATETIME_FORMAT")

        self.assertEqual(admin.display_publication_end(news), publication_end_value)

    def test_display_publication_dates(self):

        news = News(publication_end=timezone.now())
        news.publish()

        admin = NewsAdmin(News, '')

        publication_start_value = formats.date_format(localtime(news.publication_start, get_current_timezone()),
                                   "SHORT_DATETIME_FORMAT")

        publication_end_value = formats.date_format(localtime(news.publication_end, get_current_timezone()),
                                   "SHORT_DATETIME_FORMAT")

        self.assertIn(publication_start_value, admin.display_publication_dates(news))
        self.assertIn(publication_end_value, admin.display_publication_dates(news))

    def test_make_published(self):

        for i in range(0, 5):
            news = News()
            news.save()

        admin = NewsAdmin(News, '')

        queryset = News.not_published_objects.all()
        self.assertEqual(len(queryset), 5)

        with patch.object(NewsAdmin, 'message_user'):
            admin.make_published(request=None, queryset=queryset)

            new_queryset = News.not_published_objects.all()
            self.assertEqual(len(new_queryset), 0)

            drafted_queryset = News.draft_objects.all()
            self.assertEqual(len(drafted_queryset), 0)

            published_queryset = News.published_objects.all()
            self.assertEqual(len(published_queryset), 5)

    def test_make_unpublished(self):

        self.test_make_published()
        published_queryset = News.published_objects.all()
        self.assertEqual(len(published_queryset), 5)

        admin = NewsAdmin(News, '')

        with patch.object(NewsAdmin, 'message_user'):
            admin.make_unpublished(request=None, queryset=published_queryset)

            new_queryset = News.not_published_objects.all()
            self.assertEqual(len(new_queryset), 5)

            drafted_queryset = News.draft_objects.all()
            self.assertEqual(len(drafted_queryset), 5)

            published_queryset = News.published_objects.all()
            self.assertEqual(len(published_queryset), 0)

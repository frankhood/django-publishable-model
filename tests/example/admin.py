# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _

from publishable_model.admin import PublishableModelAdmin

from .models import News


@admin.register(News)
class NewsAdmin(PublishableModelAdmin, admin.ModelAdmin):
    DISPLAY_PUBLICATION_DATES = True

    fieldsets = (
        (None, {'fields': (
            ('title', 'content',),
        )}),
        (_('Publication'), {'fields': (('status', 'publication_start',
                                        'publication_end',),)}),
    )




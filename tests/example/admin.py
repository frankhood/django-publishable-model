# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django
from django.contrib import admin

if django.VERSION[0] < 3:
    from django.utils.translation import ungettext as ngettext
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import ngettext as ngettext
    from django.utils.translation import gettext_lazy as _

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




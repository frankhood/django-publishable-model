from django.db import models
#TODO from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from publishable_model.models import PublishableModel


class News(PublishableModel, models.Model):
    title = models.CharField(_("Title"), max_length=64, )
    content = models.TextField(_("Content"), blank=True, default="")

    def __str__(self):
        return self.title

    class Meta(PublishableModel.Meta):
        verbose_name = _('News')
        verbose_name_plural = _('News')

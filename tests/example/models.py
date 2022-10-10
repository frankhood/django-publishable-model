from django.db import models

from publishable_model.models import PublishableModel


class News(PublishableModel, models.Model):
    title = models.CharField(
        "Title",
        max_length=64,
    )
    content = models.TextField("Content", blank=True, default="")

    def __str__(self):
        return self.title

    class Meta(PublishableModel.Meta):
        """News Meta."""

        verbose_name = "News"
        verbose_name_plural = "News"

=====
Usage
=====

Inherit your models from PublishableModel:

.. code-block:: python

    from publishable_model.models import PublishableModel

    class MyModel(PublishableModel, models.Model):

        class Meta(PublishableModel.Meta):
            verbose_name = _("My Model")

Inherit your ModelAdmins from PublishableModelAdmin:

.. code-block:: python

    from publishable_model.admin import PublishableModelAdmin

    @admin.register(MyModel)
    class MyModelAdmin(PublishableModelAdmin, admin.ModelAdmin):
        # Uncomment next lines to enable automatic visualization of publication dates in list_display
        # DISPLAY_PUBLICATION_DATES = True
        # DISPLAY_PUBLICATION_START = True
        # DISPLAY_PUBLICATION_END = True

        fieldsets = (
            (None, {'fields': (
                 ...
            )}),
            (_('Publication'), {'fields': (('status', 'publication_start',
                                            'publication_end',),)}),
        )


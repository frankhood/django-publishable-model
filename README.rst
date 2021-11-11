=============================
Django Publishable Model
=============================

.. image:: https://badge.fury.io/py/django-publishable-model.svg
    :target: https://badge.fury.io/py/django-publishable-model

.. image:: https://travis-ci.org/frankhood/django-publishable-model.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-publishable-model

.. image:: https://codecov.io/gh/frankhood/django-publishable-model/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-publishable-model

Make your models publishable in an easy way, the admin will be smart and easily configurable

Documentation
-------------

The full documentation is at https://django-publishable-model.readthedocs.io.

Quickstart
----------

Install Django Publishable Model::

    pip install django-publishable-model

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'publishable_model',
        ...
    )


Features
--------

* Handle of Django Model's publication.

Example of usage
----------------
.. code-block:: python

    from publishable_model.models import PublishableModel

    class News(PublishableModel, models.Model):
        title = models.CharField(_("Title"), max_length=64, )
        content = models.TextField(_("Content"), blank=True, default="")

        def __str__(self):
            return self.title

        class Meta(PublishableModel.Meta):
            verbose_name = _('News')
            verbose_name_plural = _('News')


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

    or

    ./manage.py test tests


Development commands
---------------------

::
    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

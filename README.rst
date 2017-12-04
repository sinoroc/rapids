..


.. contents::

.. sectnum::


Introduction
============

**REST APIs documented and sensible**

Build automatically documented REST APIs with the `Pyramid framework`_.

This library is available on the Python package index under the project name
``rapids``:

* https://pypi.python.org/pypi/rapids

* https://pypi.org/project/rapids/


Usage
=====

.. code:: python

    @rapids.decorators.resource('', None)
    class Root(rapids.resources.Base):
        pass


    @pyramid.view.view_config(context=Root, rapids='')
    def root_view(resource, request):
        return pyramid.httpexceptions.HTTPNotFound()


    @rapids.decorators.resource('foo', Root)
    class Foo(rapids.resources.Base):
        pass


    @pyramid.view.view_defaults(context=Foo, rapids='')
    class FooView:
        def __init__(self, resource, request):
            pass

        @pyramid.view.view_config(request_method='GET')
        def _get_view(self):
            return pyramid.httpexceptions.HTTPOk()

        @pyramid.view.view_config(request_method='POST')
        def _post_view(self):
            return pyramid.httpexceptions.HTTPCreated()


Hacking
=======

This project makes extensive use of `tox`_, `pytest`_, and `GNU Make`_.


Development environment
-----------------------

Use following command to create a Python virtual environment with all
necessary dependencies::

    tox --recreate -e develop

This creates a Python virtual environment in the ``.tox/develop`` directory. It
can be activated with the following command::

    . .tox/develop/bin/activate


Run test suite
--------------

In a Python virtual environment run the following command::

    make review

Outside of a Python virtual environment run the following command::

    tox --recreate


Build and package
-----------------

In a Python virtual environment run the following command::

    make package

Outside of a Python virtual environment run the following command::

    tox --recreate -e package


.. Links

.. _`GNU Make`: https://www.gnu.org/software/make/
.. _`Pyramid framework`: https://trypyramid.com/
.. _`pytest`: http://pytest.org/
.. _`tox`: https://tox.readthedocs.io/


.. EOF

""" Functional test for decorators
"""


import unittest

import pyramid
import rapids
import webtest

import base


@rapids.decorators.resource('', None)
class Root(rapids.resources.Base):
    """ Root resource
    """
    # pylint: disable=too-few-public-methods
    member = 'FlagRoot'


def root_view(resource, unused_request):
    """ View for the root resource
    """
    return pyramid.httpexceptions.HTTPOk(resource.member)


@rapids.decorators.resource('foo', Root)
class Foo(rapids.resources.Base):
    """ Foo resource
    """
    # pylint: disable=too-few-public-methods
    member = 'FlagFoo'


@rapids.decorators.view(Foo)
def foo_view(resource, unused_request):
    """ View for the Foo resource
    """
    return pyramid.httpexceptions.HTTPOk(resource.member)


@rapids.decorators.resource('bar', Root)
class Bar(rapids.resources.Base):
    """ Bar resource
    """
    # pylint: disable=too-few-public-methods
    member = 'FlagBar'


@rapids.decorators.view(Bar)
class BarView:
    """ View for the Bar resource
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, resource, unused_request):
        self._resource = resource
        return

    def __call__(self):
        return pyramid.httpexceptions.HTTPOk(self._resource.member)


class TestDecorators(base.Base, unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(settings=self.settings)
        self.config.include(rapids.config)
        self.config.rapids_add_view(root_view, Root)
        self.config.scan()
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def test_resource_decorator(self):
        """ GET on a decorated resource returns a successful response
        """
        response = self.test_application.get('/', status=200)
        self.assertIn(Root.member, response.text)
        return

    def test_view_function_decorator(self):
        """ View decorator on a function should work
        """
        response = self.test_application.get('/foo', status=200)
        self.assertIn(Foo.member, response.text)
        return

    def test_view_class_decorator(self):
        """ View decorator on a class callable should work
        """
        response = self.test_application.get('/bar', status=200)
        self.assertIn(Bar.member, response.text)
        return


# EOF

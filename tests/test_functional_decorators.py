""" Functional test for decorators
"""


import unittest

import pyramid
import rapids
import webtest

import base


@rapids.decorators.resource('', None)
class _Root(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    member = 'FlagRoot'


def _root_view(resource, unused_request):
    return pyramid.httpexceptions.HTTPOk(resource.member)


@rapids.decorators.resource('foo', _Root)
class _Foo(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    member = 'FlagFoo'


@rapids.decorators.view(context=_Foo)
def _foo_view(resource, unused_request):
    return pyramid.httpexceptions.HTTPOk(resource.member)


@rapids.decorators.resource('bar', _Root)
class _Bar(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    member = 'FlagBar'


@rapids.decorators.view(context=_Bar)
class _BarView:
    # pylint: disable=too-few-public-methods
    def __init__(self, resource, unused_request):
        self._resource = resource
        return

    def __call__(self):
        return pyramid.httpexceptions.HTTPOk(self._resource.member)


@rapids.decorators.resource('foobar', _Root)
class _Foobar(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    member = 'FlagFoobar'


@rapids.decorators.view_defaults(context=_Foobar)
class _FoobarView:
    # pylint: disable=too-few-public-methods

    def __init__(self, resource, unused_request):
        self._resource = resource
        return

    @rapids.decorators.view(request_method='GET')
    def _get_view(self):
        return pyramid.httpexceptions.HTTPOk(self._resource.member)

    @rapids.decorators.view(request_method='POST')
    def _post_view(self):
        return pyramid.httpexceptions.HTTPCreated(self._resource.member)


class TestDecorators(base.Base, unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(settings=self.settings)
        self.config.include(rapids.config)
        self.config.rapids_add_view(view=_root_view, context=_Root)
        self.config.scan('.')
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def test_resource_decorator(self):
        """ GET on a decorated resource returns a successful response
        """
        response = self.test_application.get('/', status=200)
        self.assertIn(_Root.member, response.text)
        return

    def test_view_function_decorator(self):
        """ View decorator on a function should work
        """
        response = self.test_application.get('/foo', status=200)
        self.assertIn(_Foo.member, response.text)
        return

    def test_view_class_decorator(self):
        """ View decorator on a class callable should work
        """
        response = self.test_application.get('/bar', status=200)
        self.assertIn(_Bar.member, response.text)
        return

    def test_view_defaults_decorator(self):
        """ view_defaults decorator on a class combined with view decorator on
            the methods works
        """
        response = self.test_application.get('/foobar', status=200)
        self.assertIn(_Foobar.member, response.text)
        response = self.test_application.post('/foobar', status=201)
        self.assertIn(_Foobar.member, response.text)
        return


# EOF

""" Functional test
"""


import unittest

import rapids
import pyramid.testing
import pyramid.view
import webtest


class Resource(rapids.resources.Base):
    """ Base resource class
    """
    # pylint: disable=too-few-public-methods

    def view(self, unused_request):
        """ Default view
        """
        return pyramid.httpexceptions.HTTPOk(self.__name__)


@rapids.decorators.resource('', None)
class Root(Resource):
    """ Root resource
    """
    # pylint: disable=too-few-public-methods
    pass


@rapids.decorators.resource('foo', Root)
class Foo(Resource):
    """ Foo resource
    """
    # pylint: disable=too-few-public-methods
    pass


class Bar(Resource):
    """ Bar resource
    """
    # pylint: disable=too-few-public-methods
    pass


@pyramid.view.view_config(context=Root)
def root_view(resource, request):
    """ View for the root resource
    """
    return resource.view(request)


@pyramid.view.view_config(context=Foo)
def foo_view(resource, request):
    """ View for the foo resource
    """
    return resource.view(request)


@pyramid.view.view_config(context=Bar)
def bar_view(resource, request):
    """ View for the bar resource
    """
    return resource.view(request)


@pyramid.view.view_config(context=pyramid.httpexceptions.HTTPException)
def http_exception_view(http_exception, unused_request):
    """ View for HTTP exceptions
    """
    return http_exception


class TestFunctional(unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp()
        self.config.include('rapids.config')
        self.config.add_resource(Bar, 'bar{num}', Root)
        self.config.scan('.')
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def tearDown(self):
        pyramid.testing.tearDown()
        return

    def test_get(self):
        """ Test GET method on endpoints
        """
        self.test_application.get('/', status=200)
        self.test_application.get('/foo', status=200)
        self.test_application.get('/barone', status=200)
        self.test_application.get('/bartwo', status=200)
        self.test_application.get('/bazthree', status=404)
        return


# EOF

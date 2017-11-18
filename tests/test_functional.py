""" Functional test
"""


import unittest

import rapids
import pyramid.testing
import pyramid.view
import yaml
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
        settings = {
            'rapids.title': "test",
        }
        self.config = pyramid.testing.setUp(settings=settings)
        self.config.include('rapids.config')
        self.config.rapids_add_resource(Bar, 'bar{num}', Root)
        self.config.scan('.')
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def tearDown(self):
        pyramid.testing.tearDown()
        return

    def test_get_root(self):
        """ Root gives a valid response
        """
        self.test_application.get('/', status=200)
        return

    def test_get_subresource(self):
        """ Subresource gives a valid response
        """
        response = self.test_application.get('/foo', status=200)
        self.assertIn('foo', response.text)
        return

    def test_get_with_uri_parameterss(self):
        """ Resource with URI parameters gives a valid response
        """
        response = self.test_application.get('/barone', status=200)
        self.assertIn('barone', response.text)
        response = self.test_application.get('/bartwo', status=200)
        self.assertIn('bartwo', response.text)
        return

    def test_get_invalid_resource(self):
        """ Invalid resource responds with 404
        """
        self.test_application.get('/bazthree', status=404)
        return

    def test_document_raml(self):
        """ A valid RAML document is generated
        """
        util = self.config.registry.getUtility(rapids.utility.IUtility)
        raml_document = util.get_document('application/raml+yaml')
        raml_dict = yaml.load(raml_document)
        self.assertIn('/', raml_dict)
        self.assertIn('/foo', raml_dict['/'])
        return


# EOF

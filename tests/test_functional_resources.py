""" Functional test for resources
"""


import unittest

import pyramid
import rapids
import yaml
import webtest

import base


class Root(rapids.resources.Base):
    """ Root resource
    """
    # pylint: disable=too-few-public-methods
    pass


class Foo(rapids.resources.Base):
    """ Foo resource
    """
    # pylint: disable=too-few-public-methods
    pass


class Bar(rapids.resources.Base):
    """ Bar resource
    """
    # pylint: disable=too-few-public-methods
    pass


def root_view(resource, unused_request):
    """ View for the root resource
    """
    return pyramid.httpexceptions.HTTPOk(resource.__name__)


def http_exception_view(http_exception, unused_request):
    """ View for HTTP exceptions
    """
    return http_exception


class TestFunctional(base.Base, unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(settings=self.settings)
        self.config.include('rapids.config')
        self.config.rapids_add_resource(Root, '', None)
        self.config.rapids_add_resource(Foo, 'foo', Root)
        self.config.rapids_add_resource(Bar, 'bar{num}', Root)
        self.config.rapids_add_view(root_view, Root)
        self.config.rapids_add_view(root_view, Foo)
        self.config.rapids_add_view(root_view, Bar)
        self.config.add_view(
            http_exception_view,
            context=pyramid.httpexceptions.HTTPException,
        )
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
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
        self.assertIn('/bar{num}', raml_dict['/'])
        return


# EOF

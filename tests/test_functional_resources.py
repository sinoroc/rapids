""" Functional test for resources
"""


import unittest

import pyramid
import rapids
import yaml
import webtest

import base


class _Root(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


class _Foo(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


class _Bar(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


def _root_view(resource, unused_request):
    return pyramid.httpexceptions.HTTPOk(resource.__name__)


def _http_exception_view(http_exception, unused_request):
    return http_exception


class TestFunctional(base.Base, unittest.TestCase):
    """ Functional test
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(settings=self.settings)
        self.config.include('rapids.config')
        self.config.rapids_add_resource(_Root, '', None)
        self.config.rapids_add_resource(_Foo, 'foo', _Root)
        self.config.rapids_add_resource(_Bar, 'bar{num}', _Root)
        self.config.rapids_add_view(view=_root_view, context=_Root)
        self.config.rapids_add_view(view=_root_view, context=_Foo)
        self.config.rapids_add_view(view=_root_view, context=_Bar)
        self.config.add_view(
            _http_exception_view,
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
        self.assertIn('get', raml_dict['/'])
        self.assertIn('/foo', raml_dict['/'])
        self.assertIn('get', raml_dict['/']['/foo'])
        self.assertIn('/bar{num}', raml_dict['/'])
        self.assertIn('get', raml_dict['/']['/bar{num}'])
        return


# EOF

""" Functional test for resources
"""


import unittest

import pyramid
import yaml
import webtest

import base
import rapids  # should be considered as a 3rd party import (isort issue?)


class _Root(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


class _Foo(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


class _Bar(rapids.resources.Base):
    # pylint: disable=too-few-public-methods
    pass


def _common_view(resource, unused_request):
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
        self.config.rapids_add_resource(
            _Bar,
            'bar{num}',
            _Root,
            uri_parameters={
                'num': {
                    'type': 'integer',
                },
            },
        )
        self.config.add_view(view=_common_view, context=_Root, rapids='')
        self.config.add_view(view=_common_view, context=_Foo, rapids='')
        self.config.add_view(view=_common_view, context=_Bar, rapids='')
        self.config.add_view(
            _http_exception_view,
            context=pyramid.httpexceptions.HTTPException,
        )
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return

    def test_root(self):
        """ Root gives a valid response
        """
        self.test_application.get('/', status=200)
        return

    def test_subresource(self):
        """ Subresource gives a valid response
        """
        response = self.test_application.get('/foo', status=200)
        self.assertIn('foo', response.text)
        return

    def test_uri_parameters(self):
        """ Resource with URI parameters gives a valid response
        """
        response = self.test_application.get('/bar1', status=200)
        self.assertIn('bar1', response.text)
        response = self.test_application.get('/bar2', status=200)
        self.assertIn('bar2', response.text)
        return

    def test_uri_parameter_wrong_type(self):
        """ Resource with URI parameter of the wrong type gives a "bad request"
        """
        self.test_application.get('/barthree', status=400)
        return

    def test_uri_parameter_missing(self):
        """ Resource with URI parameter missing gives a "not found"
        """
        self.test_application.get('/bar', status=404)
        return

    def test_invalid_resource(self):
        """ Invalid resource gives a "not found"
        """
        self.test_application.get('/nowhere', status=404)
        return

    def test_document_openapi(self):
        """ A valid OpenAPI document is generated
        """
        util = self.config.registry.getUtility(rapids.utility.IUtility)
        document_raw = util.get_document('application/openapi+yaml')
        document_dict = yaml.load(document_raw)
        expected_dict = {
            'openapi': '3.0.0',
            'info': {
                'title': self.settings['rapids.title'],
            },
            'paths': {
                '/': {
                    'get': {},
                    '/foo': {
                        'get': {},
                    },
                    '/bar{num}': {
                        'parameters': [{
                            'in': 'path',
                            'name': 'num',
                            'required': True,
                            'schema': {
                                'type': 'integer',
                            },
                        }],
                        'get': {},
                    },
                },
            },
        }
        self.assertDictEqual(document_dict, expected_dict)
        return

    def test_document_raml(self):
        """ A valid RAML document is generated
        """
        util = self.config.registry.getUtility(rapids.utility.IUtility)
        document_raw = util.get_document('application/raml+yaml')
        document_dict = yaml.load(document_raw)
        expected_dict = {
            'title': self.settings['rapids.title'],
            '/': {
                'get': {},
                '/foo': {
                    'get': {},
                },
                '/bar{num}': {
                    'uriParameters': {
                        'num': {
                            'type': 'integer',
                        },
                    },
                    'get': {},
                },
            },
        }
        self.assertDictEqual(document_dict, expected_dict)
        return


# EOF

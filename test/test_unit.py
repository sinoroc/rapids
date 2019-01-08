""" Functional test
"""


import unittest

import pyramid.testing
import zope.interface

import base
import rapids  # should be considered as a 3rd party import (isort issue?)


class TestProjectVersion(unittest.TestCase):
    """ Project version string
    """
    def test_project_has_version_string(self):
        """ Project should have a vesion string
        """
        try:
            rapids.__version__
        except AttributeError as version_exception:
            self.fail(version_exception)


class TestAddResource(base.Base, unittest.TestCase):
    """ Add resources
    """

    def setUp(self):
        self.config = pyramid.testing.setUp()
        self.config.include('rapids.config')

    def test_add_valid_resource(self):
        """ Valid resources should be successfully added
        """
        class _ValidResource(
                # pylint: disable=too-few-public-methods
                rapids.resources.Base,
        ):
            pass
        try:
            self.config.rapids_add_resource(_ValidResource, '', None)
        except zope.interface.exceptions.DoesNotImplement as invalid_exception:
            self.fail(invalid_exception)

    def test_add_invalid_resource(self):
        """ Invalid resources should not be added
        """
        class _InvalidResource(
                # pylint: disable=too-few-public-methods
        ):
            pass
        with self.assertRaises(zope.interface.exceptions.DoesNotImplement):
            self.config.rapids_add_resource(_InvalidResource, '', None)


# EOF

""" Base utility pieces of code for tests
"""


import pyramid


class Base:
    """ Base class useable as a mixin for test cases
    """
    # pylint: disable=too-few-public-methods

    settings = {
        'rapids.title': "test",
    }

    def tearDown(self):
        # pylint: disable=invalid-name, no-self-use, missing-docstring
        pyramid.testing.tearDown()


# EOF

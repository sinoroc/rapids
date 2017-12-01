""" Exceptions """


import pyramid
import pyramid.httpexceptions  # should not be needed


class UriParameterWrongType(pyramid.httpexceptions.HTTPBadRequest):
    """ URI parameter has the wrong type """
    # pylint: disable=too-many-ancestors
    pass


class UriParameterUnknownType(pyramid.httpexceptions.HTTPBadRequest):
    """ URI parameter has an unknown type """
    # pylint: disable=too-many-ancestors
    pass


# EOF

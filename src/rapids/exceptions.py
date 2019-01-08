""" Exceptions """


import pyramid
import pyramid.httpexceptions  # should not be needed


class UriParameterWrongType(
        # pylint: disable=too-many-ancestors
        pyramid.httpexceptions.HTTPBadRequest,
):
    """ URI parameter has the wrong type
    """


class UriParameterUnknownType(
        # pylint: disable=too-many-ancestors
        pyramid.httpexceptions.HTTPBadRequest,
):
    """ URI parameter has an unknown type
    """


# EOF

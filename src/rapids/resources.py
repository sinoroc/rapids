""" Resources

    URI segments are the actual segments within the URLs from incoming HTTP
    requests.
    URI segment patterns are the URI segments with replacement markers (such
    as 'marco{polo}ping{pong}').
    URI segment regexes are the regexes that allow matching incoming URI
    segments to a specific URI segment pattern.
"""


import re

import zope.interface
import zope.interface.verify  # Should not be needed.

from . import exceptions


class IResource(zope.interface.Interface):
    """ Interface for resources
    """
    # pylint: disable=inherit-non-class

    __name__ = zope.interface.Attribute("""URI segment aka traversal name""")
    __parent__ = zope.interface.Attribute("""Parent resource object""")

    request = zope.interface.Attribute("""Pyramid request object""")

    def __init__(request, parent_object, uri_segment, uri_parameters):
        """ Initializer takes:
            Pyramid request object
            parent resource (an instantiated object, not a class)
            URI segment
            URI parameters (a dict)
        """
        # pylint: disable=no-self-argument,super-init-not-called
        # pylint: disable=unused-argument
        return


@zope.interface.implementer(IResource)
class Base:
    """ Base resource
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, request, parent_object, uri_segment, uri_parameters):
        self.__name__ = uri_segment
        self.__parent__ = parent_object
        self.request = request
        self._uri_parameters = uri_parameters
        return


class Manager:
    """ Resources manager
        The '_resources_tree' member is a tree-ish structure:
        {
            None: {
                r'...regex for empty string...': {
                    'resource_class': <class Root>,
                    'uri_segment_pattern': '',
                },
            },
            <class Root>: {
                r'...uri_segment_regex...': {
                    'resource_class': <class Foo>,
                    'uri_segment_pattern': 'foo',
                },
                r'...uri_segment_regex...': {
                    'resource_class': <class Bar>,
                    'uri_segment_pattern': 'bar{var}',
                },
            },
            <class Foo>: { ... },
            <class Bar>: { ... },
        }
    """

    def __init__(self, config):
        self._config = config
        self._resources_tree = {}
        self._resources_map = {}
        self._root_uri_segment_regex = _build_uri_segment_regex('')
        return

    @property
    def resources_tree(self):
        """ Resources tree
        """
        return self._resources_tree

    def add_resource(
            self,
            resource_class,
            uri_segment_pattern,
            parent_class,
            uri_parameters=None,
    ):
        """ Add resource at this URI segment pattern under this parent class
        """
        zope.interface.verify.verifyClass(IResource, resource_class)
        uri_segment_regex = _build_uri_segment_regex(uri_segment_pattern)
        resource_class.__getitem__ = self._get_child_resource_factory()
        resource_config = self._resources_map.setdefault(resource_class, {})
        resource_config['resource_class'] = resource_class
        resource_config['uri_parameters'] = uri_parameters or {}
        resource_config['uri_segment_pattern'] = uri_segment_pattern
        uri_segment_regexes = self._resources_tree.setdefault(parent_class, {})
        uri_segment_regexes[uri_segment_regex] = resource_config
        return

    def add_view(self, **kwargs):
        """ Add view to the internal structure
        """
        resource_config = self._resources_map.setdefault(kwargs['context'], {})
        request_method = kwargs.get('request_method', None) or 'get'
        resource_config.setdefault('methods', {})[request_method.lower()] = {}
        return

    def view(self, view_callable, *args, **kwargs):
        """ Derived view callable
        """
        # pylint: disable=no-self-use
        # * do some pre processing (verify input)
        # result = pre_process(...)
        # * call the view callable
        result = view_callable(*args, **kwargs)
        # * do some post processing (verify output)
        # result = post_process(...)
        # * render output according to media type
        # result = render(...)
        return result

    def _get_child_resource_factory(self):
        def _get_child_resource_wrapped(*args, **kwargs):
            return self._get_child_resource(*args, **kwargs)
        return _get_child_resource_wrapped

    def _get_child_resource(self, parent_object, uri_segment):
        child_object = None
        candidates = self._resources_tree[type(parent_object)]
        for (uri_segment_regex, resource_config) in candidates.items():
            uri_parameters = _match_uri_segment_regex(
                uri_segment_regex,
                uri_segment,
            )
            if uri_parameters is not None:
                child_object = _instantiate_resource(
                    resource_config,
                    parent_object.request,
                    parent_object,
                    uri_segment,
                    uri_parameters,
                )
                break
        if child_object is None:
            raise KeyError()
        return child_object

    def get_root(self, request):
        """ Get Pyramid traversal root resource object
        """
        root_object = _instantiate_resource(
            self._resources_tree[None][self._root_uri_segment_regex],
            request,
            parent_object=None,
            uri_segment='',
            uri_parameters=None,
        )
        return root_object


def _build_uri_segment_regex(uri_segment_pattern):
    regex_tokens = []
    split_regex = r'(\{[a-zA-Z][^\}]*\})'
    uri_tokens = re.compile(split_regex).split(uri_segment_pattern)
    for (idx, uri_token) in enumerate(uri_tokens):
        if idx % 2 == 1:
            regex_tokens.append('(?P<{}>[^/]+)'.format(uri_token[1:-1]))
        else:
            regex_tokens.append(uri_token)
    return re.compile(''.join(regex_tokens) + '$')


def _match_uri_segment_regex(uri_segment_regex, uri_segment):
    uri_parameters = None
    matched = uri_segment_regex.match(uri_segment)
    if matched is not None:
        uri_parameters = matched.groupdict()
    return uri_parameters


def _instantiate_resource(
        resource_config,
        request,
        parent_object,
        uri_segment,
        uri_parameters,
):
    _validate_uri_parameters(resource_config, uri_parameters)
    resource_object = resource_config['resource_class'](
        request,
        parent_object,
        uri_segment,
        uri_parameters,
    )
    zope.interface.verify.verifyObject(IResource, resource_object)
    return resource_object


def _validate_uri_parameters(resource_config, uri_parameters):
    for (name, config) in resource_config['uri_parameters'].items():
        value = uri_parameters[name]
        _validate_uri_parameter(value, config)
    return


def _validate_uri_parameter(value, config):
    default_type = 'string'
    ptype = config.get('type', default_type)
    if ptype == 'integer':
        if value.isdigit() is False:
            raise exceptions.UriParameterWrongType()
    elif ptype == 'string':
        pass
    else:
        raise exceptions.UriParameterUnknownType()
    return


# EOF

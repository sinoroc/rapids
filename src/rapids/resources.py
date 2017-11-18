""" Resources
"""


import re

import zope.interface
import zope.interface.verify  # Should not be needed.


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
        self.uri_parameters = uri_parameters
        return


class Manager:
    """ Resources manager
        The resources are stored in a dict. The key is the class of the
        resource. The value is a dict containing the resource class again, the
        parent class, the URI segment, the corresponding regex and a dict of
        the children. The dict of children has the URI segment regex as key and
        the child class as value.
        {
            <class Root>: {
                'resource_class': <class Root>,
                'parent_class': None,
                'uri_segment': '',
                'uri_segment_regex': '...',
                'children': {
                    '...regex..': <class Foo>,
                },
            },
            <class Foo>: { ... },
        }
    """

    def __init__(self):
        self._resources = {}
        self._root_resource_class = None
        return

    @property
    def resources(self):
        """ Resources
        """
        return self._resources

    def add_resource(self, resource_class, uri_segment, parent_class):
        """ Add resource at this URI segment under this parent class
        """
        zope.interface.verify.verifyClass(IResource, resource_class)
        uri_segment_regex = self._build_uri_segment_regex(uri_segment)
        resource_class.__getitem__ = self._get_child_resource_factory()
        children_class = {}
        for (other_class, other) in self._resources.items():
            if other_class is parent_class:
                other['children_class'][uri_segment_regex] = resource_class
            if other['parent_class'] is resource_class:
                children_class[other['uri_segment_regex']] = other_class
        self._resources[resource_class] = {
            'children_class': children_class,
            'parent_class': parent_class,
            'resource_class': resource_class,
            'uri_segment': uri_segment,
            'uri_segment_regex': uri_segment_regex,
        }
        if uri_segment == '' and parent_class is None:
            self._root_resource_class = resource_class
        return

    def _get_child_resource_factory(self):
        def _get_child_resource(*args, **kwargs):
            return self.get_child_resource(*args, **kwargs)
        return _get_child_resource

    def get_child_resource(self, parent_object, uri_segment):
        """ Get child resource instance
            Instantiate a child resource object of this parent resource object
            corresponding to this URI segment.
        """
        child_object = None
        children_class = self._resources[type(parent_object)]['children_class']
        for (uri_segment_regex, resource_class) in children_class.items():
            uri_parameters = self._match_uri_segment_regex(
                uri_segment_regex,
                uri_segment,
            )
            if uri_parameters is not None:
                resource = self._resources[resource_class]
                child_object = self._instantiate_resource(
                    resource,
                    parent_object.request,
                    parent_object,
                    uri_segment,
                    uri_parameters,
                )
                break
        if child_object is None:
            raise KeyError()
        return child_object

    def root_factory(self, request):
        """ Root factory for Pyramid traversal
        """
        root_resource = self._resources[self._root_resource_class]
        root_object = self._instantiate_resource(
            root_resource,
            request,
            parent_object=None,
            uri_segment='',
            uri_parameters={},
        )
        return root_object

    @staticmethod
    def _build_uri_segment_regex(uri_segment):
        regex_tokens = []
        uri_tokens = re.compile(r'(\{[a-zA-Z][^\}]*\})').split(uri_segment)
        for (idx, uri_token) in enumerate(uri_tokens):
            if idx % 2 == 1:
                regex_tokens.append('(?P<{}>[^/]+)'.format(uri_token[1:-1]))
            else:
                regex_tokens.append(uri_token)
        return re.compile(''.join(regex_tokens) + '$')

    @staticmethod
    def _match_uri_segment_regex(uri_segment_regex, uri_segment):
        uri_parameters = None
        matched = uri_segment_regex.match(uri_segment)
        if matched is not None:
            uri_parameters = matched.groupdict()
        return uri_parameters

    @staticmethod
    def _instantiate_resource(
            resource,
            request,
            parent_object,
            uri_segment,
            uri_parameters,
    ):
        """ Instantiate a resource
        """
        resource_object = resource['resource_class'](
            request,
            parent_object,
            uri_segment,
            uri_parameters
        )
        zope.interface.verify.verifyObject(IResource, resource_object)
        return resource_object


# EOF

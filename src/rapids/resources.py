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
    __parent__ = zope.interface.Attribute("""Parent resource""")

    request = zope.interface.Attribute("""Pyramid request object""")

    def __init__(request, parent, uri_segment, uri_parameters):
        """ Initializer takes:
            Pyramid request object
            parent resource
            URI segment
            URI parameters (a dict)
        """
        # pylint: disable=no-self-argument,super-init-not-called
        # pylint: disable=unused-argument
        return


@zope.interface.implementer(IResource)
class Base:  # pylint: disable=too-few-public-methods
    """ Base resource
    """

    def __init__(self, request, parent, uri_segment, uri_parameters):
        self.__name__ = uri_segment
        self.__parent__ = parent
        self.request = request
        self.uri_parameters = uri_parameters
        return


def root_factory(request):
    """ Root factory for Pyramid traversal
    """
    manager = request.registry.getUtility(IManager)
    return manager.root_factory(request)


class IManager(zope.interface.Interface):
    """ Interface for the resources manager utility
    """
    # pylint: disable=inherit-non-class
    pass


@zope.interface.implementer(IManager)
class Manager:
    """ Resources manager utility
    """

    def __init__(self):
        self._resources = []
        return

    def add_resource(self, resource, uri_segment, parent):
        """ Add resource
            resource is a class
            uri_segment is a pattern (curly braces)
            parent is a class
        """
        zope.interface.verify.verifyClass(IResource, resource)
        regex = self._build_regex(uri_segment)
        resource.__getitem__ = self._get_child_resource
        self._resources.append({
            'parent': parent,
            'regex': regex,
            'resource': resource,
            'uri_segment': uri_segment,
        })
        return

    def root_factory(self, request):
        """ Root factory for Pyramid traversal
        """
        root = None
        for resource_iter in self._resources:
            if resource_iter['parent'] is None:
                root = self._instantiate(
                    resource_iter,
                    request,
                    parent=None,
                    uri_segment='',
                    uri_parameters={},
                )
                break
        return root

    def get_child_resource(self, resource, uri_segment):
        """ Get child resource of this resource for this URI segment
        """
        children = []
        item = None
        for resource_iter in self._resources:
            if (resource_iter['parent'] is not None and
                    isinstance(resource, resource_iter['parent'])):
                children.append(resource_iter)
        for child in children:
            uri_parameters = self._match(child['regex'], uri_segment)
            if uri_parameters is not None:
                item = self._instantiate(
                    child,
                    resource.request,
                    parent=resource,
                    uri_segment=uri_segment,
                    uri_parameters=uri_parameters,
                )
                break
        return item

    @staticmethod
    def _build_regex(uri_segment):
        regex_tokens = []
        uri_tokens = re.compile(r'(\{[a-zA-Z][^\}]*\})').split(uri_segment)
        for (idx, uri_token) in enumerate(uri_tokens):
            if idx % 2 == 1:
                regex_tokens.append('(?P<{}>[^/]+)'.format(uri_token[1:-1]))
            else:
                regex_tokens.append(uri_token)
        return re.compile(''.join(regex_tokens) + '$')

    @staticmethod
    def _match(regex, uri_segment):
        result = None
        matched = regex.match(uri_segment)
        if matched is not None:
            result = matched.groupdict()
        return result

    @staticmethod
    def _get_child_resource(resource, uri_segment):
        """ Get child resource of this resource for this URI segment
        """
        manager = resource.request.registry.getUtility(IManager)
        return manager.get_child_resource(resource, uri_segment)

    @staticmethod
    def _instantiate(resource, request, parent, uri_segment, uri_parameters):
        """ Instantiate a resource
        """
        instance = resource['resource'](
            request,
            parent,
            uri_segment,
            uri_parameters
        )
        zope.interface.verify.verifyObject(IResource, instance)
        return instance


# EOF

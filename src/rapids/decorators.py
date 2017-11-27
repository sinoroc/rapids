""" Decorators
"""


import inspect

import venusian

from . import exceptions
from . import utility


def resource(*args, **kwargs):
    """ Class decorator
        The decorated class is added as a resource.
    """
    return _ResourceHelper(*args, **kwargs)


class _ResourceHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, uri_segment_pattern, parent_class):
        self._uri_segment_pattern = uri_segment_pattern
        self._parent_class = parent_class
        return

    def __call__(self, resource_class):
        venusian.attach(resource_class, self._callback)
        return resource_class

    def _callback(self, scanner, unused_name, resource_class):
        """ Callback for venusian
            Venusian is useful to have access to the Pyramid configuration
            from a decorator. This happens when the scan is performed.
        """
        util = scanner.config.registry.getUtility(utility.IUtility)
        util.add_resource(
            resource_class,
            self._uri_segment_pattern,
            self._parent_class,
        )
        return


def view_defaults(**kwargs):
    """ Decorator allowing to set defaults for the view decorator
        This decorator should be used on classes to provide defaults for the
        view decorator set on the methods.
    """
    return _ViewDefaultsHelper(**kwargs)


class _ViewDefaultsHelper:
    # pylint: disable=too-few-public-methods

    VIEW_DEFAULTS_ATTRIBUTE_NAME = '__rapids_view_defaults_attr__'

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        return

    def __call__(self, view_class):
        setattr(view_class, self.VIEW_DEFAULTS_ATTRIBUTE_NAME, self._kwargs)
        return view_class


def view(**kwargs):
    """ Decorator allowing to add views
        This decorator works on functions, callable classes and when used
        with view_defaults on methods as well.
    """
    return _ViewHelper(**kwargs)


class _ViewHelper:
    # pylint: disable=too-few-public-methods

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._view_callable = None
        self._view_class_callable_method = None
        return

    def __call__(self, decorated):
        venusian_info = venusian.attach(
            decorated,
            self._callback,
        )  # pylint: disable=no-member
        if venusian_info.scope == 'class':
            self._view_class_callable_method = decorated
        return decorated

    def _callback(self, scanner, unused_name, view_callable):
        self._view_callable = view_callable
        view_config = {}
        if self._view_class_callable_method is not None:
            view_config.update(getattr(
                self._view_callable,
                _ViewDefaultsHelper.VIEW_DEFAULTS_ATTRIBUTE_NAME,
                {},
            ))
        view_config.update(self._kwargs)
        view_config['view'] = self._wrapped_view_callable
        util = scanner.config.registry.getUtility(utility.IUtility)
        util.add_view(**view_config)
        return

    def _wrapped_view_callable(self, *args, **kwargs):
        result = None
        if self._view_class_callable_method is not None:
            instance = self._view_callable(*args, **kwargs)
            result = self._view_class_callable_method(instance)
        elif inspect.isclass(self._view_callable):
            # view callable is a class callable
            result = self._view_callable(*args, **kwargs)()
        elif inspect.isfunction(self._view_callable):
            # view callable is a function
            result = self._view_callable(*args, **kwargs)
        else:
            raise exceptions.ViewCallableInvalid()
        return result


# EOF

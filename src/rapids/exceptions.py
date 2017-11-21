""" Exceptions
"""


class ViewCallableInvalid(Exception):
    """ Exception raised when the view callable can not be properly called
        Probably it is not possible to figure out what kind of callable has
        been decorated (function or callable class).
    """
    pass


# EOF

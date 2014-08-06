"""Exception classes.
"""


class InvalidMethod(Exception):
    """Raised when an invalid pydash method is invoked through
    :func:`pydash.api.chaining.chain`.
    """
    pass

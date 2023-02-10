"""
Utils for deprecating our code using warning.warn().
The warning message is written to stderr when shown.

For the difference between DeprecationWarning
and other deprecation warning classes, refer to
https://peps.python.org/pep-0565/#additional-use-case-for-futurewarning

If external packages import deprecated interfaces,
it is their responsibility to detect and remove them.
"""
import warnings
from functools import wraps
from typing import Callable, Optional, TypeVar

RT = TypeVar("RT")  # return type


def _make_message(message: str, replacement: Optional[str]) -> str:
    return f"{message}, please use {replacement}" if replacement else message


def deprecated(replacement: Optional[str]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Mark a function/method as deprecated.

    The warning is shown by default when triggered directly
    by code in __main__.
    """

    def decorator(func: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> RT:  # type: ignore
            warning_message = _make_message(
                f"{func.__name__} is deprecated and will be removed in a future release", replacement
            )
            # Setting stacklevel=2 to let Python print the line that calls
            # this wrapper, not the line below.
            warnings.warn(warning_message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
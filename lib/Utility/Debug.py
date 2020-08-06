import functools

from ..Output import Out
def Debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def __INTERNAL__(*args, **kwargs):
        Out.VerbosePrint(Out.Verbosity.MEDIUM, f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        Out.VerbosePrint(Out.Verbosity.MEDIUM, f"{func.__name__!r} returned")
        return value
    return __INTERNAL__


def DebugClassMethod(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def __INTERNAL__(*args, **kwargs):
        args_repr = repr(args[0])
        Out.VerbosePrint(Out.Verbosity.MEDIUM, f"Calling {func.__name__}({args_repr})")
        value = func(*args, **kwargs)
        Out.VerbosePrint(Out.Verbosity.MEDIUM, f"{func.__name__!r}({args_repr}) returned")
        return value
    return __INTERNAL__    
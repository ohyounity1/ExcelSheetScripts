import functools
import time

from ..Output import Out

def Timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def __INTERNAL__(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        Out.VerbosePrint(Out.Verbosity.MEDIUM, f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return __INTERNAL__
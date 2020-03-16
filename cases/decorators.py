from functools import wraps


def skip_when_testing(func=None):
    """
    Stubs out the method if test

    Note:
        taken from here: https://gist.github.com/kevinastone/7295567
    """
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            import sys
            # Look for harvest or test for testing environments
            if set(('test', 'harvest')) & set(sys.argv):
                return
            # Also break if we're running within nose
            for arg in sys.argv:
                if 'nosetests' in arg:
                    return
            return func(*args, **kwargs)
        return wrapped
    if func:
        return wrapper(func)
    else:
        return wrapper
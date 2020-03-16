from functools import wraps


def skip_when_testing(func=None):
    """
    Stubs out the method if test

    Note:
        taken from here: https://gist.github.com/kevinastone/7295567
    """
    ARGS_TO_IGNORE = ['nosetests', 'makemigrations', 'migrate']

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            import sys
            print(sys.argv)
            # Look for harvest or test for testing environments
            if set(('test', 'harvest')) & set(sys.argv):
                return
            for arg in ARGS_TO_IGNORE:
                if arg in sys.argv:
                    return
            return func(*args, **kwargs)
        return wrapped
    if func:
        return wrapper(func)
    else:
        return wrapper


def only_run_on_server(func=None):
    """
    Stubs out the method if not running on server

    Note:
        taken from here: https://gist.github.com/kevinastone/7295567
    """
    # test that gunicorn actually works
    ACTIVE_ARGS = ['runserver', 'gunicorn']

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            import sys
            # Look for harvest or test for testing environments
            for arg in ACTIVE_ARGS:
                if arg in sys.argv:
                    return func(*args, **kwargs)
            return
        return wrapped
    if func:
        return wrapper(func)
    else:
        return wrapper
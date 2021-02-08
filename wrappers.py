from functools import wraps


def cmd():

    def cmd_decorator(func):

        @wraps(func)
        def cmd_wrapper(*args):
            return func(*args)

        cmd_wrapper.isCommand = True
        return cmd_wrapper

    return cmd_decorator


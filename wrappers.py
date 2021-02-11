from functools import wraps


def cmd():
    def cmd_decorator(func):
        @wraps(func)
        def cmd_wrapper(*args):
            return func(*args)

        cmd_wrapper.is_command = True
        return cmd_wrapper

    return cmd_decorator

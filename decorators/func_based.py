from datetime import datetime
from functools import wraps
from time import sleep
from typing import Callable


def no_args_logger(func: Callable):
    """Logger decorator without args"""

    @wraps(func)  # preserve func name/docstring
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print(f"Start {func.__name__} at {start}")

        res = func(*args, **kwargs)

        end = datetime.now()
        duration = end - start
        print(f"End {func.__name__} at {end}. Duration is {duration}")

        return res

    return wrapper


def logger(*log_args, **log_kwargs):
    """Logger decorator with args"""

    def logger_wrapper(func: Callable):
        @wraps(func)
        def func_wrapper(*func_args, **func_kwargs):
            start = datetime.now()
            print(
                f"Start {func.__name__} at {start}. "
                f"Decorator args={log_args}, kwargs={log_kwargs}"
            )

            if "delay" in log_kwargs:
                sleep(log_kwargs["delay"])

            res = func(*func_args, **func_kwargs)

            end = datetime.now()
            duration = end - start
            print(f"End {func.__name__} at {end}. Duration is {duration}")

            return res

        return func_wrapper

    return logger_wrapper


@no_args_logger
def foo(*args, **kwargs):
    print(f"hello! {args}, {kwargs}")
    sleep(0.5)


@logger("timer", delay=1)
def bar(*args, **kwargs):
    print(f"hello! {args}, {kwargs}")
    sleep(0.5)


def main():
    assert foo.__name__ == "foo"
    foo(1, a="aaa!")

    assert bar.__name__ == "bar"
    bar(2, b="bbb!")


if __name__ == "__main__":
    main()

import copy
import functools
from datetime import datetime
from time import sleep
from typing import Callable


class no_args_logger:
    def __init__(self, func: Callable):
        self._func = func
        functools.update_wrapper(self, func)  # preserve func name/docstring

    def __call__(self, *func_args, **func_kwargs):
        start = datetime.now()
        print(f"Start {self._func.__name__} at {start}")

        res = self._func(*func_args, **func_kwargs)

        end = datetime.now()
        duration = end - start
        print(f"End {self._func.__name__} at {end}. Duration is {duration}")

        return res


class logger:
    def __init__(self, *log_args, **log_kwargs):
        self._log_args = copy.copy(log_args)
        self._log_kwargs = log_kwargs.copy()

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def func_wrapper(*func_args, **func_kwargs):
            start = datetime.now()
            print(
                f"Start {func.__name__} at {start}. "
                f"Decorator args={self._log_args}, kwargs={self._log_kwargs}"
            )

            if "delay" in self._log_kwargs:
                sleep(self._log_kwargs["delay"])

            res = func(*func_args, **func_kwargs)

            end = datetime.now()
            duration = end - start
            print(f"End {func.__name__} at {end}. Duration is {duration}")

            return res

        return func_wrapper


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

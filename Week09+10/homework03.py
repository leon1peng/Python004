import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'function {func.__name__} take up time: {(end_time - start_time) * 1000} ms')
        return result

    return wrapper


@timer
def foo(num):
    sum_num = 0
    for i in range(num):
        sum_num += 1
    return sum_num


if __name__ == '__main__':
    foo(10)

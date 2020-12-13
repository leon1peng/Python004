def my_map(fun, *iterators):
    for nums in iterators:
        yield [fun(num) for num in nums]


def my_func(x):
    return x - 1


if __name__ == '__main__':
    result = my_map(my_func, [1, 2, 3])
    print(result)
    print(next(result))

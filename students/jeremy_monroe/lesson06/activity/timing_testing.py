from timeit import timeit

repetitions = 10000
my_range = 1000
lower_limit = my_range / 2

my_list = list(range(my_range))


def multiply_by_two(x):
    return x * 2

def greater_than_lower_limit(x):
    return x > lower_limit


print('\n\nGenerator with expressions')
print(timeit(
    'generator_test = (x * 2 for x in my_list if x > lower_limit)',
    globals=globals(),
    number=repetitions
    ))


print('\n\nGenerator with functions')
print(timeit(
    'generator_test_2 = (multiply_by_two(x) for x in my_list if greater_than_lower_limit(x))',
    globals=globals(),
    number=repetitions
    ))


print('\n\nMap filter with functions')
print(timeit(
    'map_filter_with_functions = map(multiply_by_two, filter(greater_than_lower_limit, my_list))',
    globals=globals(),
    number=repetitions
    ))


print('\n\nList comprehension with expressions')
print(timeit(
    'comprehension_test = [x * 2 for x in my_list if x > lower_limit]',
    globals=globals(),
    number=repetitions
    ), '\n\n')

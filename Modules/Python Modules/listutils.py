# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'listutils'

import random

def length(lst):
    return len(lst)

def is_empty(lst):
    return len(lst) == 0

def copy(lst):
    return lst.copy()

def clear(lst):
    lst.clear()
    return lst

def reverse(lst):
    return lst[::-1]

def sort(lst):
    return sorted(lst)

def sort_reverse(lst):
    return sorted(lst, reverse=True)

def append(lst, item):
    lst.append(item)
    return lst

def insert(lst, index, item):
    lst.insert(index, item)
    return lst

def extend(lst, other):
    lst.extend(other)
    return lst

def remove(lst, item):
    lst.remove(item)
    return lst

def remove_at(lst, index):
    del lst[index]
    return lst

def pop(lst):
    return lst.pop()

def pop_at(lst, index):
    return lst.pop(index)

def contains(lst, item):
    return item in lst

def count(lst, item):
    return lst.count(item)

def index_of(lst, item):
    return lst.index(item)

def find(lst, item):
    try:
        return lst.index(item)
    except ValueError:
        return -1

def first(lst):
    return lst[0]

def last(lst):
    return lst[-1]

def get(lst, index):
    return lst[index]

def set_at(lst, index, value):
    lst[index] = value
    return lst

def slice(lst, start, end):
    return lst[start:end]

def sum_list(lst):
    return sum(lst)

def average(lst):
    if not lst:
        return 0
    return sum(lst) / len(lst)

def minimum(lst):
    return min(lst)

def maximum(lst):
    return max(lst)

def product(lst):
    result = 1

    for item in lst:
        result *= item

    return result

def random_choice(lst):
    return random.choice(lst)

def random_sample(lst, amount):
    return random.sample(lst, amount)

def shuffle(lst):
    temp = lst.copy()
    random.shuffle(temp)
    return temp

def unique(lst):
    return list(dict.fromkeys(lst))

def duplicates(lst):
    seen = set()
    dupes = []

    for item in lst:
        if item in seen and item not in dupes:
            dupes.append(item)
        seen.add(item)

    return dupes

def join(lst, separator):
    return separator.join(
        str(x)
        for x in lst
    )

def split(text, separator):
    return text.split(separator)

def remove_none(lst):
    return [
        x
        for x in lst
        if x is not None
    ]

def remove_empty(lst):
    return [
        x
        for x in lst
        if x != ""
    ]

def remove_duplicates(lst):
    return unique(lst)

def all_true(lst):
    return all(lst)

def any_true(lst):
    return any(lst)

def none_true(lst):
    return not any(lst)

def range_list(start, end):
    return list(range(start, end))

def repeated(value, count):
    return [value] * count

def zeros(count):
    return [0] * count

def ones(count):
    return [1] * count

def concat(a, b):
    return a + b

def zip_lists(a, b):
    return list(zip(a, b))

def flatten(lst):
    result = []

    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)

    return result

def rotate_left(lst, steps=1):
    steps %= len(lst)
    return lst[steps:] + lst[:steps]

def rotate_right(lst, steps=1):
    steps %= len(lst)
    return lst[-steps:] + lst[:-steps]

def frequency(lst):
    result = {}

    for item in lst:
        result[item] = (
            result.get(item, 0) + 1
        )

    return result

def median(lst):
    data = sorted(lst)

    n = len(data)

    if n == 0:
        return None

    if n % 2:
        return data[n // 2]

    return (
        data[n // 2 - 1]
        + data[n // 2]
    ) / 2

def mode(lst):
    counts = frequency(lst)

    return max(
        counts,
        key=counts.get
    )
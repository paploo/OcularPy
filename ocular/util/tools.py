import math
import re


def map_optional(func, value):
    return func(value) if value else None


def codeize(string, placeholder='_', upper=True):
    code = string.strip()
    code = re.sub('[^A-Za-z0-9_-]', '', code)
    code = re.sub('\s+', placeholder, code)
    return code.upper() if upper else code


def snap(value, granularity):
    return math.ceil(value / granularity) * granularity


def min_by(iterable, transform):
    return min([transform(x) for x in iterable])


def max_by(iterable, transform):
    return max([transform(x) for x in iterable])
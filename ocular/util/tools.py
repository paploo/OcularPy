import re


def map_optional(func, value):
    return func(value) if value else None


def codeize(string, placeholder='_', upper=True):
    code = string.strip()
    code = re.sub('[^A-Za-z0-9_-]', '', code)
    code = re.sub('\s+', placeholder, code)
    return code.upper() if upper else code

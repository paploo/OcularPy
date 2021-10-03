class Manufacturer:

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"({self.code}) {self.name}"

    def __eq__(self, o: object):
        if isinstance(o, Manufacturer):
            return self.code == o.code
        else:
            return False


generic = Manufacturer('GEN', 'Generic')

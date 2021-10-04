class Manufacturer:

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, o: object):
        if isinstance(o, Manufacturer):
            return self.code == o.code
        else:
            return False

    def __hash__(self):
        return hash(self.code)


generic = Manufacturer('GEN', 'Generic')

class Manufacturer:

    def __init__(self, code, name):
        self.code = code
        self.name = name

    @property
    def label(self):
        """
        A nice human readable label.

        Currently this is a synonym to name for this class.
        """
        return self.name

    def __str__(self):
        return self.label

    def __eq__(self, o: object):
        if isinstance(o, Manufacturer):
            return self.code == o.code
        else:
            return False

    def __hash__(self):
        return hash(self.code)


generic = Manufacturer('GEN', 'Generic')

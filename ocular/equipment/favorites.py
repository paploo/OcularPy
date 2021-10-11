class Favorites:

    def __init__(self, code, name, kind, codes) -> object:
        self.code = code
        self.name = name
        self.kind = kind
        self.codes = codes

    def __str__(self):
        return f"Favorites(name='{self.name}', kind={self.kind.name}, codes={self.codes})"

    def __getitem__(self, index):
        return self.codes[index]

    def __iter__(self):
        return iter(self.codes)

    def __add__(self, other):
        if type(other) == Favorites and other.kind == self.kind:
            return Favorites(f"{self.code}+{other.code}",
                             f"{self.name} + {other.name}",
                             self.kind,
                             self.codes + other.codes)
        else:
            raise Exception("Cannot combine favorites")

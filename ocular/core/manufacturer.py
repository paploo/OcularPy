class Manufacturer:

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"({self.code}) {self.name}"


generic = Manufacturer("GEN", "Generic")

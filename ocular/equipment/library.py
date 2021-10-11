from enum import Enum


class CatalogKind(Enum):
    TELESCOPE = 'TELESCOPE'
    EYEPIECE = 'EYEPIECE'
    FAVORITES = 'FAVORITES'


class Library:
    """
    A named library of any kind of content that has a code.

    This provides a wrapper for metadata to go along with the underlying dict of code to item.

    This is typically used to manage catalogs of equipment, such as telescopes and eyepieces, but is more abstract.
    For example, a library of favorites lists can be managed using this same class.
    """

    def __init__(self, name, kind, catalog):
        self.name = name
        self.kind = kind
        self.catalog = catalog

    def __getitem__(self, key):
        return self.catalog[key]

    def __iter__(self):
        return iter(self.catalog.values())


    def filter_favorites(self, favorites):
        return self.__class__(f"{favorites.name} from {self.name}",
                              self.kind,
                              {k: v for k, v in self.catalog.items() if k in favorites.codes})

    def __str__(self):
        return f"Library(name='{self.name}', kind={self.kind.name}, catalog={self.catalog.keys()})"

    @classmethod
    def with_items(cls, name, kind, items):
        return cls(name,
                   kind,
                   {item.code: item for item in items})

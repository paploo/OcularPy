from pathlib import Path
from ocular.equipment import csv_loader
from ocular.equipment import sample_loader


def main():
    p = Path('./equipment/eyepieces.csv')
    eyepieces = csv_loader.load_eyepieces(p)
    print([str(e) for e in eyepieces])

    telescopes = sample_loader.load_telescopes(None)
    print([str(t) for t in telescopes])


if __name__ == '__main__':
    main()

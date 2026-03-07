#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nasumicno bira pitanja iz foldera cesta_pitanja.

Parametri (svi neobavezni):
  --poglavlje N    bira pitanja samo iz datog poglavlja (npr. 10)
  --broj N         ukupan broj pitanja za izbor (podrazumevano: sva u opsegu)
"""

import argparse
import os
import random

BASE = os.path.dirname(os.path.abspath(__file__))
CESTA_PITANJA = os.path.join(BASE, "cesta_pitanja")


def parse_oznaka(filename):
    """Parsiraj oznaku iz naziva fajla i vrati (oznaka, poglavlje, sort_kljuc)."""
    if not filename.endswith(".txt"):
        return None

    stem = filename[:-4]
    parts = stem.split(".")
    if len(parts) < 3 or parts[0] != "0":
        return None

    try:
        numbers = [int(p) for p in parts]
    except ValueError:
        return None

    oznaka = ".".join(str(n) for n in numbers)
    poglavlje = numbers[1]
    return oznaka, poglavlje, tuple(numbers)


def naslov_pitanja(path):
    """Cita prvu nepraznu liniju kao naslov pitanja."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                text = line.strip()
                if text:
                    return text
    except OSError:
        return None
    return None


def dostupna_pitanja():
    """Vraca listu dict objekata: oznaka, poglavlje, sort_kljuc, path."""
    if not os.path.isdir(CESTA_PITANJA):
        return []

    result = []
    for name in os.listdir(CESTA_PITANJA):
        parsed = parse_oznaka(name)
        if parsed is None:
            continue
        oznaka, poglavlje, sort_kljuc = parsed
        result.append(
            {
                "oznaka": oznaka,
                "poglavlje": poglavlje,
                "sort_kljuc": sort_kljuc,
                "path": os.path.join(CESTA_PITANJA, name),
            }
        )
    result.sort(key=lambda x: x["sort_kljuc"])
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Nasumicno bira pitanja iz foldera cesta_pitanja."
    )
    parser.add_argument(
        "--poglavlje",
        type=int,
        default=None,
        metavar="N",
        help="Bira pitanja samo iz zadatog poglavlja (npr. 10)",
    )
    parser.add_argument(
        "--broj",
        type=int,
        default=None,
        metavar="N",
        help="Koliko pitanja nasumicno izabrati",
    )
    args = parser.parse_args()

    sva = dostupna_pitanja()
    if not sva:
        print("U folderu cesta_pitanja nema prepoznatih .txt fajlova pitanja.")
        return 1

    if args.poglavlje is not None:
        u_rasponu = [q for q in sva if q["poglavlje"] == args.poglavlje]
        raspon_tekst = f"poglavlje {args.poglavlje}"
    else:
        u_rasponu = sva
        raspon_tekst = "sva poglavlja"

    if not u_rasponu:
        print(f"Nema pitanja za {raspon_tekst}.")
        return 1

    koliko = args.broj if args.broj is not None else len(u_rasponu)
    if koliko <= 0:
        print("Parametar --broj mora biti veci od 0.")
        return 1

    if koliko > len(u_rasponu):
        print(
            f"U opsegu ({raspon_tekst}) ima {len(u_rasponu)} pitanja. "
            f"Trazeno je {koliko}; biram sva dostupna."
        )
        koliko = len(u_rasponu)

    izabrana = random.sample(u_rasponu, koliko)
    izabrana.sort(key=lambda x: x["sort_kljuc"])

    print(f"Izabrano {len(izabrana)} pitanja ({raspon_tekst}):\n")
    for i, q in enumerate(izabrana):
        file_name = os.path.basename(q["path"])
        print(f"--- {file_name} ---")
        naslov = naslov_pitanja(q["path"])
        if naslov is not None:
            print(naslov)
        else:
            print("(nije moguce procitati naslov)")
        if i < len(izabrana) - 1:
            print("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

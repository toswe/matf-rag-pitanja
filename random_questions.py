#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nasumično bira pitanja iz foldera pojedinacno (format grupa.broj.txt).

Parametri (svi neobavezni):
  --grupa N  tražena grupa, 1–4 (podrazumijevano: sve grupe)
  --broj N   ukupan broj pitanja za izbor (podrazumijevano: sva u grupi/grupama)
"""

import argparse
import os
import random
import re

BASE = os.path.dirname(os.path.abspath(__file__))
POJEDINACNO = os.path.join(BASE, "pojedinacno")


def naslov_pitanja(path):
    """Čita samo prvu liniju (naslov/pitanje), uklanja vodeće # i **."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            linija = f.readline().strip()
    except OSError:
        return None
    # Ukloni markdown naslove (##, ###) i **
    linija = re.sub(r"^#+\s*", "", linija)
    linija = re.sub(r"\*+", "", linija).strip()
    return linija if linija else None


def dostupna_pitanja():
    """Vraća listu (grupa, broj) za sve fajlove grupa.broj.txt."""
    if not os.path.isdir(POJEDINACNO):
        return []
    pitanja = []
    for f in os.listdir(POJEDINACNO):
        if not f.endswith(".txt"):
            continue
        base = f[:-4]  # bez .txt
        if "." in base:
            parts = base.split(".", 1)
            try:
                g, b = int(parts[0]), int(parts[1])
                if 1 <= g <= 4:
                    pitanja.append((g, b))
            except ValueError:
                continue
    return sorted(pitanja)


def main():
    parser = argparse.ArgumentParser(
        description="Nasumično bira pitanja iz foldera pojedinacno.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--grupa",
        type=int,
        default=None,
        choices=[1, 2, 3, 4],
        metavar="N",
        help="Tražena grupa pitanja (1–4)",
    )
    parser.add_argument(
        "--broj",
        type=int,
        default=None,
        metavar="N",
        help="Koliko pitanja nasumično izabrati",
    )
    args = parser.parse_args()

    sva = dostupna_pitanja()
    if not sva:
        print("U folderu pojedinacno nema fajlova grupa.broj.txt.")
        return 1

    if args.grupa is not None:
        u_rasponu = [(g, b) for g, b in sva if g == args.grupa]
        raspon_tekst = f"grupa {args.grupa}"
    else:
        u_rasponu = sva
        raspon_tekst = "sve grupe (1–4)"

    if not u_rasponu:
        print(f"Nema pitanja za {raspon_tekst}.")
        return 1

    koliko = args.broj if args.broj is not None else len(u_rasponu)
    if koliko > len(u_rasponu):
        print(
            f"U {raspon_tekst} ima {len(u_rasponu)} pitanja. "
            f"Traženo je {koliko}; biram sva dostupna."
        )
        koliko = len(u_rasponu)

    izabrana = random.sample(u_rasponu, koliko)
    izabrana.sort()

    print(f"Izabrano {len(izabrana)} pitanja ({raspon_tekst}):\n")
    for i, (g, b) in enumerate(izabrana):
        filename = f"{g}.{b}.txt"
        path = os.path.join(POJEDINACNO, filename)
        print(f"--- {filename} ---")
        naslov = naslov_pitanja(path)
        if naslov is not None:
            print(naslov)
        else:
            print("(nije moguće pročitati naslov)")
        if i < len(izabrana) - 1:
            print("\n\n")
    return 0


if __name__ == "__main__":
    exit(main())

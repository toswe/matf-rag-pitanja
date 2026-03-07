#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nasumično bira pitanja iz foldera pojedinacno (format grupa.broj.txt ili grupa.broj.znam.txt).

Parametri (svi neobavezni):
  --grupa N         tražena grupa, 1–4 (podrazumijevano: sve grupe)
  --broj N           ukupan broj pitanja za izbor (podrazumijevano: sva u grupi/grupama)
  --preskaci-znam    ne biraj pitanja označena kao „znam“ (postoji grupa.broj.znam.txt)
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
    """Vraća listu (grupa, broj) za fajlove grupa.broj.txt i grupa.broj.znam.txt."""
    if not os.path.isdir(POJEDINACNO):
        return []
    pitanja = set()
    for f in os.listdir(POJEDINACNO):
        if not f.endswith(".txt"):
            continue
        base = f[:-4]  # bez .txt
        if base.endswith(".znam"):
            base = base[:-5]  # grupa.broj
        if "." not in base:
            continue
        parts = base.split(".", 1)
        try:
            g, b = int(parts[0]), int(parts[1])
            if 1 <= g <= 4:
                pitanja.add((g, b))
        except ValueError:
            continue
    return sorted(pitanja)


def fajl_pitanja(grupa, broj):
    """Put do fajla pitanja: grupa.broj.txt ako postoji, inače grupa.broj.znam.txt."""
    obicno = os.path.join(POJEDINACNO, f"{grupa}.{broj}.txt")
    znam = os.path.join(POJEDINACNO, f"{grupa}.{broj}.znam.txt")
    return obicno if os.path.isfile(obicno) else znam


def pitanje_oznaceno_znam(grupa, broj):
    """Da li postoji fajl grupa.broj.znam.txt."""
    return os.path.isfile(os.path.join(POJEDINACNO, f"{grupa}.{broj}.znam.txt"))


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
    parser.add_argument(
        "--preskaci-znam",
        action="store_true",
        help="Preskači pitanja označena kao „znam“ (fajl grupa.broj.znam.txt)",
    )
    args = parser.parse_args()

    sva = dostupna_pitanja()
    if not sva:
        print("U folderu pojedinacno nema fajlova grupa.broj.txt / grupa.broj.znam.txt.")
        return 1

    if args.grupa is not None:
        u_rasponu = [(g, b) for g, b in sva if g == args.grupa]
        raspon_tekst = f"grupa {args.grupa}"
    else:
        u_rasponu = sva
        raspon_tekst = "sve grupe (1–4)"

    if args.preskaci_znam:
        u_rasponu = [(g, b) for g, b in u_rasponu if not pitanje_oznaceno_znam(g, b)]
        raspon_tekst += " (bez „znam“)"

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
        path = fajl_pitanja(g, b)
        filename = os.path.basename(path)
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
